from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book

# Add book (only users with "can_add_book")
@permission_required('relationship_app.can_add_book')
def add_book(request):
    return HttpResponse("You have permission to add a book!")

# Edit book (only users with "can_change_book")
@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    return HttpResponse(f"You have permission to edit book with ID {book_id}!")

# Delete book (only users with "can_delete_book")
@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    return HttpResponse(f"You have permission to delete book with ID {book_id}!")
