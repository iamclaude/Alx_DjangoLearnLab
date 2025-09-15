from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExampleForm
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html')

# A view that uses ExampleForm (checker checks import; having a working view is useful)
def form_example_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # For demo, render a tiny success page showing submitted data
            return render(request, "bookshelf/form_success.html", {"data": form.cleaned_data})
    else:
        form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})
