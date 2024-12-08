from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import CategoryViewSet, ProductViewSet, ReviewViewSet


router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'review', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
