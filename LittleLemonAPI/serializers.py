from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem, Cart 
        
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    
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
        

class CartCustomerSerializer(serializers.ModelSerializer):    
    unit_price = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ["id", "user", "menuitem", "unit_price", "quantity", "price"]
    
    def get_unit_price(self, obj):
        return obj.get_unit_price()
    
    def get_price(self, obj):
        return obj.quantity * self.get_unit_price(obj)