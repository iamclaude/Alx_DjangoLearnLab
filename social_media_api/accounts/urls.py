# accounts/urls.py
from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),  # custom login returning token
    path('token-auth/', obtain_auth_token, name='token-auth'),  # alternative token endpoint
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
