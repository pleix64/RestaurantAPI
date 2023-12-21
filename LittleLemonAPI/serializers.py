from rest_framework import serializers
from django.contrib.auth.models import User, Group
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
        
class GroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        fields = ["id", "name"]

        
class UserSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "groups"]
        

        