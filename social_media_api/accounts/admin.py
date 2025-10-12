# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('bio', 'profile_picture', 'followers')}),
    )
    list_display = ('username', 'email', 'is_staff', 'is_active')
