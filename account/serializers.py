from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer

from account.models import CustomUser


# Create your serializers here.
class SMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class VerifySMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verification_code = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'password', 'email', 'username']
