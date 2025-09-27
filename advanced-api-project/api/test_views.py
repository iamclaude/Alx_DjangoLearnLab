from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tester', password='pass123')
        self.client.login(username='tester', password='pass123') 
        self.author = Author.objects.create(name='Chinua Achebe')
        self.book = Book.objects.create(title='Things Fall Apart', publication_year=1958, author=self.author)

    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Things Fall Apart', str(response.data))

    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'No Longer at Ease',
            'publication_year': 1960,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_unauthenticated(self):
        data = {
            'title': 'Arrow of God',
            'publication_year': 1964,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Things Fall Apart - Updated'}
        response = self.client.put(f'/api/books/{self.book.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/books/{self.book.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_books_by_year(self):
        response = self.client.get('/api/books/?publication_year=1958')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        response = self.client.get('/api/books/?search=Things')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Things Fall Apart', str(response.data))

    def test_order_books_by_title(self):
        Book.objects.create(title='A Man of the People', publication_year=1966, author=self.author)
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))


# Tests CRUD operations and query features for Book API
# Ensures permissions are enforced for create/update/delete
# Validates filtering, searching, and ordering logic
