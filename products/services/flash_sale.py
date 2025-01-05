from django.utils import timezone
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django_filters import rest_framework as dj_filters
from datetime import timedelta

from products.models import FlashSale, Product, ProductViewHistory
from products.views import CustomPagination
from products.filters import FlashSaleFilter
from products.permissions import IsStaffOrReadOnly


# Create your views here
class FlashSaleListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    queryset = FlashSale.objects.all()

    class FlashSaleSerializer(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = "__all__"

    serializer_class = FlashSaleSerializer
    pagination_class = CustomPagination

    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = FlashSaleFilter


@api_view(['get'])
def check_flash_sale(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({'error': "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    user_viewed = ProductViewHistory.objects.filter(user=request.user, product=product).exists()  # exists() -> natija bor bo'lsa True, aks holda -> False

    upcoming_flash_sale = FlashSale.objects.filter(
        product=product,
        start_time__lte=timezone.now() + timedelta(hours=24)
    ).first()

    if user_viewed and upcoming_flash_sale:
        discount = upcoming_flash_sale.discount_percentage
        start_time = upcoming_flash_sale.start_time
        end_time = upcoming_flash_sale.end_time

        return Response(
            {
                'message': f"This product will be on a {discount}% off flash sale",
                'start_time': start_time,
                'end_time': end_time,
            }, status=status.HTTP_200_OK
        )
    else:
        return Response({"message": "No upcoming flash sales for this product."}, status=status.HTTP_404_NOT_FOUND)
