# LibraryProject/relationship_app/urls.py

from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from . import views

urlpatterns = [
    # function-based view
    path('books/', list_books, name='list_books'),

    # class-based view (DetailView)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # keep other urls if you have them
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),

    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]
