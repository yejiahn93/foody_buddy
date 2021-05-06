import django_filters
from .models import *
class RestaurantFilter(django_filters.FilterSet):
    restaurant_name = django_filters.CharFilter(label='Restaurant')
    class Meta:
        model = Restaurant
        fields = ['restaurant_name']