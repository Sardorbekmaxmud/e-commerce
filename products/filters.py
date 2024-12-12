from django_filters import rest_framework as dj_filters
from products.models import Product, FlashSale, Review


class ProductFilter(dj_filters.FilterSet):
    min_price = dj_filters.NumberFilter('price', lookup_expr='gte')
    max_price = dj_filters.NumberFilter('price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']


class ReviewFilter(dj_filters.FilterSet):
    class Meta:
        model = Review
        fields = ['user', 'product', 'rating']


class FlashSaleFilter(dj_filters.FilterSet):
    start_time = dj_filters.DateFilter('start_time', lookup_expr='gte')
    end_time = dj_filters.DateFilter('end_time', lookup_expr='lte')

    class Meta:
        model = FlashSale
        fields = ['discount_percentage', 'start_time', 'end_time']
