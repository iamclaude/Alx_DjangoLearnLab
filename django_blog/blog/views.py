# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, ProfileForm, PostForm
from .models import Post, Comment
from .forms import CommentForm
from django.db.models import Q

def search_view(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, 'blog/search_results.html', {'query': query, 'results': results}) 

# --- Existing register_view and profile_view here (unchanged) ---
def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        email = request.POST.get("email", "").strip()
        if profile_form.is_valid():
            profile_form.save()
            if email:
                user.email = email
                user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        profile_form = ProfileForm(instance=user.profile)
    return render(request, "blog/profile.html", {"profile_form": profile_form, "user": user})

# --- Posts CRUD views ---

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"  # blog/post_list.html
    context_object_name = "posts"
    ordering = ["-published_date"]
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"  # blog/post_detail.html
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.select_related("author").all()
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    @transaction.atomic
    def form_valid(self, form):
        # set author then save to get instance
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # process tags from cleaned_data (list of tag names)
        tag_names = form.cleaned_data.get("tags", [])
        if tag_names:
            tags = []
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag_obj)
            self.object.tags.set(tags)
        return response

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    @transaction.atomic
    def form_valid(self, form):
        # ensure author unchanged
        form.instance.author = self.request.user
        response = super().form_valid(form)
        tag_names = form.cleaned_data.get("tags", [])
        if tag_names is not None:
            tags = []
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag_obj)
            self.object.tags.set(tags)
        return response

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    # blog/views.py (append)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    # template not used for inline creation; redirect back to post detail
    def form_valid(self, form):
        post_pk = self.kwargs.get("post_pk")
        post = get_object_or_404(Post, pk=post_pk)
        form.instance.post = post
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # redirect to the post detail page after creating comment
        return HttpResponseRedirect(reverse("post-detail", kwargs={"pk": post.pk}))

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.kwargs.get("post_pk")})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user  # keep author consistent
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})

# Tag filtered list
class TaggedPostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"  # reuse list template
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get("tag_name", "").lower()
        return Post.objects.filter(tags__name=tag_name).order_by("-published_date")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag_filter"] = self.kwargs.get("tag_name", "")
        return ctx

# Search view (function-based for simplicity)
def search_view(request):
    q = request.GET.get("q", "").strip()
    results = Post.objects.none()
    if q:
        # search in title, content, and tag names (case-insensitive)
        results = Post.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)
        ).distinct().order_by("-published_date")
    return render(request, "blog/search_results.html", {"query": q, "posts": results})

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return Post.objects.filter(tags__slug=tag_slug)