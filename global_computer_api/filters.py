from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    class Meta:
        model = Product
        # fields = ['category', 'district']
        fields = ['category__slug', 'offered', 'featured', 'side_menu__slug', 'category__title', 'brand__slug', 'is_stock', 'display_big']
