import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Payment
from products.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
class CreateChargeView(APIView):
    def post(self, request, *args, **kwargs):
        stripe_token = request.data.get('stripe_token')
        order_id = request.data.get('order_id')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'order not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            total_amount = order.product.price * order.quantity

            # to'lovni amalga oshirish
            charge = stripe.Charge.create(
                amount=int(total_amount * 100),
                currency="usd",
                source=stripe_token,
            )

            # payment jadvaliga yangi ma'lumot qo'shish
            Payment.objects.create(
                order=order,
                stripe_charge_id=charge['id'],
                amount=total_amount
            )

            # order holati to'langanga o'zgartirish
            order.is_paid = True
            order.save()

            return Response({'message': 'Payment successfully completed'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
