#from django_filters import rest_framework as filters
import django_filters
from .models import MenuItem, Order

class MenuItemFilter(django_filters.FilterSet):
    
    class Meta:
        model = MenuItem
        fields = {
            'category': ['exact'],
            'featured': ['exact'],
            'price': ['gte', 'lte']
        }
        

class OrderFilter(django_filters.FilterSet):
    delivery_crew__isnull = django_filters.BooleanFilter(field_name='delivery_crew', lookup_expr='isnull')
    
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'date': ['gte', 'lte']
        }