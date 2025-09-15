from django.urls import path
from .views import book_list

urlpatterns = [
    path("books/", book_list, name="book_list"),
    path('form/', views.form_example_view, name='form_example'),
]
