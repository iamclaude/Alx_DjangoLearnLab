# accounts/urls.py
from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),  # custom login returning token
    path('token-auth/', obtain_auth_token, name='token-auth'),  # alternative token endpoint
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
]
