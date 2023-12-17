from django.shortcuts import render
from rest_framework import generics
from .models import Category, User
from .serializers import CategorySerializer, UsersSerializer

class UsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    