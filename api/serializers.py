"""
Serializers for Author and Book models.

- BookSerializer: serializes all Book fields and validates publication_year.
- AuthorSerializer: includes 'name' and a nested list of the author's books via BookSerializer.
"""

from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    Validates that publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Ensure the publication year is not in the future.
        """
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model that includes a nested list of the author's books.
    The 'books' field is read-only and uses the BookSerializer to serialize related Book objects.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
