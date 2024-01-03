from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem, Cart, Order, OrderItem
        
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
    
    
class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
    

class OrderTotalField(serializers.Field):
    
    def to_internal_value(self, data):
        return super().to_internal_value(data)


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    delivery_crew = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(groups__name="Delivery Crew"), 
                                                       allow_null=True, 
                                                       default=None)
    dishes = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'dishes']
        
    def get_request_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user
    
class OrderUpdateSerializer(serializers.ModelSerializer):
    dishes = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id','user', 'delivery_crew', 'status', 'total', 'date', 'dishes']
        read_only_fields = ['id','user', 'delivery_crew', 'total', 'date', 'dishes']

