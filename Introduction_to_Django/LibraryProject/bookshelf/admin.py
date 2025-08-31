from django.contrib import admin
from .models import Book

# Customize the admin interface for Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns shown in list view
    search_fields = ('title', 'author')  # Search bar for title and author
    list_filter = ('publication_year',)  # Filter sidebar for publication year
