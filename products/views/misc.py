from rest_framework.viewsets import ModelViewSet
from rest_framework import pagination, filters, permissions
from django_filters import rest_framework as dj_filters
from products.models import Category, Review, Order
from products.serializers import CategorySerializer, ReviewSerializer, OrderSerializer
from products.filters import ReviewFilter
from products.permissions import IsOwnerOrReadOnly


# Create your views here.
class CustomPagination(pagination.PageNumberPagination):
    page_size = 3


class CategoryViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    filter_backends = [dj_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ReviewFilter
    search_fields = ['content',]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
