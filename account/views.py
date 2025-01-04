from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
import random
import requests

from .serializers import SMSSerializer, VerifySMSSerializer

User = get_user_model()
SMS_KEY = settings.SMS_KEY


# Create your views here.
class SMSLoginViewSet(viewsets.ViewSet):
    def send_sms(self, request):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            verification_code = str(random.randint(100000, 999999))

            url = 'https://4e29v1.api.infobip.com/sms/2/text/advanced'
            headers = {
                'Authorization': f'App {SMS_KEY}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            payload = {
                'messages': [
                    {
                        'from': 'ChoyxonaExpress',
                        'destinations': [{'to': str(phone_number).replace('+', '')}],
                        'text': f'Your verification code is {verification_code}'
                    }
                ]
            }
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                cache.set(phone_number, verification_code, 300)

                return Response({'message': 'SMS sent successfully'}, status=status.HTTP_200_OK)

            return Response({'message': 'Failed to sent SMS'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def verify_sms(self, request):
        serializer = VerifySMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']

            cached_code = cache.get(phone_number)

            if verification_code == cached_code:
                user, created = User.objects.get_or_create(phone_number=phone_number)
                if created:
                    # Yaratilgan user uchun email va username qo'shish
                    email = serializer.validated_data.get('email', None)
                    username = serializer.validated_data.get('username', None)

                    if email:
                        user.email = email
                    if username:
                        user.username = username

                    user.save()

                else:
                    # user allaqachon mavjud bo'lsa, email va username yangilanadi
                    email = serializer.validated_data.get('email', user.email)
                    username = serializer.validated_data.get('username', user.username)

                    user.email = email
                    user.username = username
                    user.save()

                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                )

            return Response({'message': 'Invalid verfication code'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
