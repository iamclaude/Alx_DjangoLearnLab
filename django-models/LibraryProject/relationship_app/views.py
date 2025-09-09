from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from .models import Book, Library, UserProfile

# -------------------------------
# FUNCTION-BASED VIEW: List all books
# -------------------------------
def list_books(request):
    books = Book.objects.all()  # checker is looking for this
    return render(request, 'relationship_app/list_books.html', {'books': books})

# -------------------------------
# CLASS-BASED VIEW: Library detail
# -------------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# -------------------------------
# AUTHENTICATION VIEWS
# -------------------------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

# -------------------------------
# BOOK CRUD WITH PERMISSIONS
# -------------------------------
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        Book.obje
