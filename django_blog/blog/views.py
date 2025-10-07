# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib import messages

def register_view(request):
    """
    Handle a new user registration.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, "Registration successful.")
            return redirect("profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile_view(request):
    """
    Simple profile view to let the user see and update their email.
    """
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if email:
            request.user.email = email
            request.user.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
        else:
            messages.error(request, "Please provide a valid email.")
    return render(request, "blog/profile.html", {"user": request.user})
