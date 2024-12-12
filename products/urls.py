from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import CategoryViewSet, ProductViewSet, ReviewViewSet
from .services.flash_sale import FlashSaleListCreateView, check_flash_sale
from .services.product_view_history import ProductViewHistoryListCreate


router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'review', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sale/', FlashSaleListCreateView.as_view(), name="sale"),
    path('check-sale/<int:product_id>/', check_flash_sale, name='check-sale'),
    path('product-view/', ProductViewHistoryListCreate.as_view(), name='product-view-history-list-create'),
]
