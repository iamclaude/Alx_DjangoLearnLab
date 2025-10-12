# accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import CustomUser  

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

# Registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # token already created in serializer.create()
        token = Token.objects.get(user=user)
        data = UserSerializer(user, context={'request': request}).data
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)

# Login view that returns token
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')
        # try username first
        user = authenticate(request, username=username, password=password)
        if user is None:
            # allow login via email
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        data = UserSerializer(user, context={'request': request}).data
        data['token'] = token.key
        return Response(data)

# Profile (retrieve & update)
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # profile of current authenticated user
        return self.request.user
    
class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response({'detail': "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(target_user)
        return Response({'detail': f'You are now following {target_user.username}.'}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response({'detail': "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.remove(target_user)
        return Response({'detail': f'You unfollowed {target_user.username}.'}, status=status.HTTP_200_OK)
