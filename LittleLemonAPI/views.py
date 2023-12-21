from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem
from .serializers import (CategorySerializer, MenuItemSerializer,
                          UserSerializer, )

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
        