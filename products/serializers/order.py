from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from rest_framework import serializers
from dotenv import load_dotenv
import os

from products.models import Order, Product

load_dotenv()


# Create your serializers here.
class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'product', 'customer', 'quantity', 'created_at', 'total_price', 'phone_number']

    @staticmethod
    def get_total_price(obj):
        return obj.product.price * obj.quantity

    def validate_quantity(self, value):
        try:
            product_id = self.initial_data['product']
            product = Product.objects.get(id=product_id)

            if value > product.stock:
                raise serializers.ValidationError("Not enough items in stock.")

            if value < 0:
                raise serializers.ValidationError("Quantity must be at least 1.")

            return value

        except ObjectDoesNotExist:
            raise serializers.ValidationError("Product does not exist.")

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        product = order.product
        product.stock -= order.quantity
        product.save()
        self.send_confirmation_email(order)
        return order

    @staticmethod
    def send_confirmation_email(order):
        title = f"Hurmatli {order.customer.username}!"
        message = f"Sizning buyurtma raqami:🆔{order.id} bo'lgan 📦 buyurtmangiz 📥 qabul qilindi!\n" \
                  f"📦 Buyurtmangizni belgilangan 🕒 vaqt oralig'ida 📤 yetkazib beramiz!😊"
        to_email = User.objects.get(id=order.customer.id, is_active=True)

        send_mail(subject=title,
                  message=message,
                  from_email=os.getenv('EMAIL_HOST_USER'),
                  recipient_list=[to_email.email],
                  fail_silently=False)
