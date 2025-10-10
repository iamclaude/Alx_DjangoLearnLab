# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "profile_picture")
        widgets = {"bio": forms.Textarea(attrs={"rows": 3})}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")  # author/published_date handled in view
        widgets = {
            "title": forms.TextInput(attrs={"maxlength": 200}),
            "content": forms.Textarea(attrs={"rows": 10}),
        }
