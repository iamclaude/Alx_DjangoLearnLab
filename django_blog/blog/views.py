# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        email = request.POST.get("email", "").strip()
        if profile_form.is_valid():
            profile_form.save()
            if email:
                user.email = email
                user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        profile_form = ProfileForm(instance=user.profile)
    return render(request, "blog/profile.html", {"profile_form": profile_form, "user": user})
