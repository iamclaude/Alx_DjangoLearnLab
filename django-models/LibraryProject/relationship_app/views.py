from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library


# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()  # <- this exact line is required
    output = ", ".join([f"{book.title} by {book.author.name}" for book in books])
    return HttpResponse(output)


# Class-based view: Display details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
