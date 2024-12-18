from rest_framework import serializers
from products.models import Category, Review, Product, ProductViewHistory


# Create your serializers here.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'price', 'stock', 'avg_rating']


class ProductViewHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViewHistory
        fields = "__all__"
