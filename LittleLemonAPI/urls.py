from django.urls import path, include
from .views import (CategoryListView, 
                    CategoryDetailView,
                    MenuItemListView, 
                    MenuItemDetailView,
                    user_group, 
                    user_group_remove, 
                    CartListView,
                    OrderListView,
                    OrderDetailView)

app_name = "api"
urlpatterns = [
    path('', include('djoser.urls')),
    path('categories', CategoryListView.as_view()),
    path('categories/<int:pk>', CategoryDetailView.as_view()),
    path('menu-items', MenuItemListView.as_view()),
    path('menu-items/<int:pk>', MenuItemDetailView.as_view()),
    path('groups/<str:groupname>/users', user_group),
    path('groups/<str:groupname>/users/<int:userID>', user_group_remove),
    path('cart/menu-items', CartListView.as_view(), name='cart'), 
    path('orders', OrderListView.as_view()),
    path('orders/<int:pk>', OrderDetailView.as_view()),
]