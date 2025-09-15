from django.contrib import admin
from .models import CustomUser, Book

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "date_of_birth")

admin.site.register(CustomUser, CustomUserAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")

admin.site.register(Book, BookAdmin)
