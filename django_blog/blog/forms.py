# blog/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    ModelForm for Post creation & editing.
    The 'author' is set in the view (not in the form).
    """
    class Meta:
        model = Post
        fields = ['title', 'content']  # author and published_date handled automatically
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
