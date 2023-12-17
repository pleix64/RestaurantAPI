from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category

class UsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "groups", "user_permissions"]
        

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ["title", "slug"]
