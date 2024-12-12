from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import pagination, filters
from django_filters import rest_framework as dj_filters
from django.db import models
from products.models import Category, Product, Review
from products.serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from products.filters import ProductFilter, ReviewFilter


# Create your views here.
class CustomPagination(pagination.PageNumberPagination):
    page_size = 3


class CategoryViewSet(ModelViewSet):
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


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    filter_backends = [dj_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)

        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializer = ProductSerializer(related_products, many=True)

        return Response({
                'product': serializer.data,
                'related_products': related_serializer.data,
            })

    @action(detail=False, methods=['get'])
    def top_rating(self, request):
        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')[:2]

        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()

        if reviews.count() == 0:
            return Response({'avg_rating': 'No reviews yet!'})

        avg_rating = sum([review.rating for review in reviews]) / reviews.count()

        return Response({
            'average_rating': avg_rating
        })
