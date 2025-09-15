from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('create/', views.create_book, name='create_book'),
    path('edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
]
