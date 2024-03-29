from typing import Any
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (IsAuthenticated, 
                                        DjangoModelPermissions,
                                        DjangoModelPermissionsOrAnonReadOnly, )
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem, Cart, Order
from .serializers import (CategorySerializer, 
                          MenuItemSerializer,
                          UserSerializer, 
                          CartSerializer,
                          OrderItemSerializer,
                          OrderSerializer, 
                          OrderCreateSerializer,
                          OrderManagerSerializer,
                          OrderDeliveryCrewSerializer)
from .filters import MenuItemFilter, OrderFilter
    
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    
class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    filterset_class = MenuItemFilter
    search_fields = ['title']
    ordering_fields = ['title', 'price']
    
class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_group(request, groupname):
    if not (request.user.groups.filter(name="Manager").exists() or request.user.is_superuser):
        return Response({"message": "Not Authorized."}, status=status.HTTP_403_FORBIDDEN)

    groupname = groupname.replace('-', ' ').title()
    if request.method=='GET':
        if not Group.objects.filter(name=groupname).exists():
            return Response({"message": "User group not found. Please enter 'manager' or 'delivery-crew' in url path between '/groups/' and '/users'."},
                            status=status.HTTP_404_NOT_FOUND)
        queryset = User.objects.filter(groups__name=groupname)
        serialized = UserSerializer(queryset, many=True)
        return Response(serialized.data)
    elif request.method=='POST':
        data = request.data
        if "username" in data:
            username = data["username"]
            user = get_object_or_404(User, username=username)
            group = get_object_or_404(Group, name=groupname)
            group.user_set.add(user)
            group.save()
            serialized = UserSerializer(user, many=False)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Please provide the username that you want to add as Manager."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_group_remove(request, groupname, userID):
    if not (request.user.groups.filter(name="Manager").exists() or request.user.is_superuser):
        return Response({"message": "Not Authorized."}, status=status.HTTP_403_FORBIDDEN)
    
    groupname = groupname.replace('-', ' ').title()
    user = get_object_or_404(User, pk=userID)
    group = get_object_or_404(Group, name=groupname)
    group.user_set.remove(user)
    group.save()
    serialized = UserSerializer(user, many=False)
    return Response(serialized.data, status=status.HTTP_200_OK)
        
        
class CartListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def get_queryset(self):
        userID = self.request.user.id
        return Cart.objects.filter(user=userID)
    
    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        self.perform_destroy(queryset)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OrderListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    search_fields = ['user__username', 'delivery_crew__username']
    ordering_fields = ['status', 'date']
    
    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew__exact=self.request.user.id)
        else:
            return Order.objects.filter(user__exact=self.request.user.id)
        
    def get_serializer_class(self):
        if (not (self.request.user.groups.filter(name='Manager').exists() or 
                self.request.user.groups.filter(name="Delivery Crew").exists()) 
            and self.request.method=='POST'):
            return OrderCreateSerializer
        else:
            return OrderSerializer
        
    def create(self, request, *args, **kwargs):
        # check authentication and retrieve cart data     
        headers = None
        if request.auth:
            headers = {'Authorization': f'Token {request.auth}'}
        elif request.user.auth_token:
            headers = {'Authorization': f'Token {request.user.auth_token.key}'}
        else:
            return Response({"message": "Not authenticated to retrieve cart items."}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        domain = 'http://127.0.0.1:8000'
        cart_path = reverse("api:cart")
        response = requests.get(domain + cart_path, headers=headers)
        cart_data = response.json()
        
        # create new order 
        order_serializer = self.get_serializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)
        self.perform_create(order_serializer)
                    
        # create order items data
        if len(cart_data)==0:
            return Response({"message": "Cannot place order when cart is empty."},
                            status=status.HTTP_403_FORBIDDEN)
        
        order_items = []
        for row in cart_data:
            item = row.copy()
            item.pop("id")
            if "user" in item.keys():
                item.pop("user")
            item["order"] = order_serializer.data["id"]
            order_items.append(item)
            
        order_item_serializer = OrderItemSerializer(data=order_items, many=True)
        order_item_serializer.is_valid(raise_exception=True)
        self.perform_create(order_item_serializer)
        
        # no need of return for OrderItem headers, just run in case of error raising
        self.get_success_headers(order_item_serializer.data) 
        response_headers = self.get_success_headers(order_serializer.data)

        # clear cart
        requests.delete(domain + cart_path, headers=headers)
        
        # return serialized Order with nested OrderItems
        result_obj = get_object_or_404(self.get_queryset(), pk=order_serializer.data["id"])
        result_serializer = OrderSerializer(result_obj)
        return Response(result_serializer.data, status=status.HTTP_201_CREATED, headers=response_headers)

        
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissions]
    
    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew__exact=self.request.user.id)
        else:
            return Order.objects.filter(user__exact=self.request.user.id)
    
    def get_serializer_class(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return OrderManagerSerializer
        elif self.request.user.groups.filter(name="Delivery Crew").exists():
            return OrderDeliveryCrewSerializer
        else:
            return OrderSerializer