from django.urls import path
from .views import (CategoryListView, CategoryDetailView,
                    MenuItemListView, MenuItemDetailView, )

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('categories/<int:pk>', CategoryDetailView.as_view()),
    path('menu-items/', MenuItemListView.as_view()),
    path('menu-items/<int:pk>', MenuItemDetailView.as_view()),
]