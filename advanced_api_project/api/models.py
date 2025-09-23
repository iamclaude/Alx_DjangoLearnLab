"""
Models for the api app.

Author: stores an author's name.
Book: stores book info and references an Author (one-to-many).
"""

from django.db import models

class Author(models.Model):
    """
    Author model: stores the author's name.
    The related_name 'books' allows accessing author.books.all() for related Book objects.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model: stores title, publication year, and references an Author.
    - title: book title
    - publication_year: integer year of publication
    - author: foreign key to Author, related_name='books'
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        # helpful representation for admin and shells
        return f"{self.title} ({self.publication_year})"
