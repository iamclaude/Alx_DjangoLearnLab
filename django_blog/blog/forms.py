# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Tag
from .models import Comment

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
    tags = forms.CharField(required=False, help_text="Comma-separated tags (e.g. django,python,help)")

    class Meta:
        model = Post
        fields = ("title", "content", "tags")
        widgets = {
            "title": forms.TextInput(attrs={"maxlength": 200}),
            "content": forms.Textarea(attrs={"rows": 10}),
        }

    def clean_tags(self):
        raw = self.cleaned_data.get("tags", "")
        # normalize: split, strip, lower, remove empties, unique
        tag_list = []
        for t in [s.strip() for s in raw.split(",") if s.strip()]:
            if t:
                tag_list.append(t.lower())
        # preserve order but unique
        seen = set()
        unique_tags = []
        for t in tag_list:
            if t not in seen:
                seen.add(t)
                unique_tags.append(t)
        return unique_tags

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment..."}),
        }
        labels = {"content": ""}
