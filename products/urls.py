from .signals import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import CategoryViewSet, ProductViewSet, ReviewViewSet, OrderViewSet
from .services.flash_sale import FlashSaleListCreateView, check_flash_sale
from .services.product_view_history import ProductViewHistoryListCreate
from .services.replenish_stock import admin_replenish_stock


router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sale/', FlashSaleListCreateView.as_view(), name="sale"),
    path('check-sale/<int:product_id>/', check_flash_sale, name='check-sale'),
    path('product-view/', ProductViewHistoryListCreate.as_view(), name='product-view-history-list-create'),
    path('admin/replenish_stock/<int:product_id>/<int:amount>/', admin_replenish_stock, name='admin-replenish-stock')
]
