from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem
        
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "featured", "category"]