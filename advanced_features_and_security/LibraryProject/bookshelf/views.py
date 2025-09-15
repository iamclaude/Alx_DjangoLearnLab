from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required("bookshelf.can_create", raise_exception=True)
def add_book(request):
    return render(request, "bookshelf/add_book.html")

@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request):
    return render(request, "bookshelf/edit_book.html")

@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request):
    return render(request, "bookshelf/delete_book.html")
