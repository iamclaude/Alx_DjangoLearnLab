# relationship_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("register/", views.register, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),

    # Library
    path("books/", views.book_list, name="book_list"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Role-based
    path("admin_view/", views.admin_view, name="admin_view"),
    path("librarian_view/", views.librarian_view, name="librarian_view"),
    path("member_view/", views.member_view, name="member_view"),

    # Book management
    path("add_book/", views.add_book, name="add_book"),
    path("edit_book/<int:pk>/", views.edit_book, name="edit_book"),
    path("delete_book/<int:pk>/", views.delete_book, name="delete_book"),
]
