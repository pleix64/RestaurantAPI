from django.urls import path
from .views import CategoriesView, UsersView

urlpatterns = [
    #path('users/', UsersView.as_view()),
    path('categories/', CategoriesView.as_view()),
]