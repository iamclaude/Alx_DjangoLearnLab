# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # registration
    path("register/", views.register_view, name="register"),

    # login/logout using Django's built-in auth views and templates
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),

    # profile
    path("profile/", views.profile_view, name="profile"),
]
s