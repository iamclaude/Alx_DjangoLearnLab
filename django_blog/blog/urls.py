# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # auth
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),

    # posts CRUD
    path("posts/", views.PostListView.as_view(), name="post-list"),
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),  # duplicate for convenience

    # Comments (nested under posts)
    path("post/<int:post_pk>/comments/new/", views.CommentCreateView.as_view(), name="comment-create"),
    path("post/comments/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment-update"),
    path("post/comments/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
]
