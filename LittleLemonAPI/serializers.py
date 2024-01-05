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

    groups = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "groups"]
        

class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
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
    

class OrderSerializer(serializers.ModelSerializer):
    '''A serializer for all users to List, and for Customer to Retrieve'''
    user = serializers.StringRelatedField()
    delivery_crew = serializers.StringRelatedField()
    total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    dishes = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'dishes']
        read_only_fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'dishes']
        # may need to set all to read_only to avoid logic leak from serializer class setup in View
        
    
class OrderCreateSerializer(serializers.ModelSerializer):
    '''A serializer for Customer ONLY to create an Order'''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    delivery_crew = serializers.HiddenField(allow_null=True, default=None) # Q: allow_null=True?
    status = serializers.HiddenField(default=0)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
    

class OrderManagerSerializer(serializers.ModelSerializer):
    '''A serializer for Manager to Retrieve, Update and Destroy an Order.
    Manager can update delivery_crew and status.'''
    user = serializers.StringRelatedField()
    delivery_crew = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(groups__name="Delivery Crew"))
    dishes = OrderItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    # suprisingly, this read_only=True is necessary to avoid Total showing up in the PUT form
    
    class Meta:
        model = Order
        fields = ['id','user', 'delivery_crew', 'status', 'total', 'date', 'dishes']
        read_only_fields = ['id','user', 'total', 'date', 'dishes']
        
    
class OrderDeliveryCrewSerializer(serializers.ModelSerializer):
    '''A serializer for DeliveryCrew to Retrieve and Update an Order.
    DeliveryCrew can only update status.'''
    user = serializers.StringRelatedField()
    delivery_crew = serializers.StringRelatedField()
    dishes = OrderItemSerializer(many=True, read_only=True)
    

    class Meta:
        model = Order
        fields = ['id','user', 'delivery_crew', 'status', 'total', 'date', 'dishes']
        read_only_fields = ['id','user', 'delivery_crew', 'total', 'date', 'dishes']