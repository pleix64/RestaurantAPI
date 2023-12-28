from django.urls import path
from .views import (CategoryListView, CategoryDetailView,
                    MenuItemListView, MenuItemDetailView,
                    user_group, user_group_remove, 
                    CartCustomerView,)

urlpatterns = [
    path('categories', CategoryListView.as_view()),
    path('categories/<int:pk>', CategoryDetailView.as_view()),
    path('menu-items', MenuItemListView.as_view()),
    path('menu-items/<int:pk>', MenuItemDetailView.as_view()),
    path('groups/<str:groupname>/users', user_group),
    path('groups/<str:groupname>/users/<int:userID>', user_group_remove),
    path('cart/menu-items', CartCustomerView.as_view()),
]