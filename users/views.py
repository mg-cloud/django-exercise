from django.shortcuts import render
from users.models import User
from users.serializers import UserSerializer
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
