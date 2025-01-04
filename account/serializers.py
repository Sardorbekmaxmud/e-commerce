from rest_framework import serializers


# Create your serializers here.
class SMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class VerifySMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verification_code = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
