# api/urls.py
from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Old ListAPIView (still available at /books/)
    path('books/', BookList.as_view(), name='book-list'),
    
   # Router URLs for full CRUD 
    path('', include(router.urls)),
]
