from rest_framework import serializers
from .models import Payment


# Create your serializers here.
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
