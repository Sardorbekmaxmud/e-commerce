from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime
import requests

from products.models import ProductViewHistory, FlashSale

User = get_user_model()
SMS_KEY = settings.SMS_KEY


@api_view(['get'])
@swagger_auto_schema(operation_description='Send an SMS ad to purchase a product in the category the user last viewed')
def send_sms_user_sale_product_view(request, pk=None):
    flash_sales = FlashSale.objects.all()

    sales_products_info = []
    for i in flash_sales:
        sales_products_info.append(
            {
                'product': i.product.name,
                'discount_percentage': i.discount_percentage,
                'start_time': i.start_time,
                'end_time': i.end_time
            }
        )

    product_view = ProductViewHistory.objects.filter(user=pk).order_by('-timestamp').first()
    phone_number_and_text = {}

    phone_number = product_view.user.phone_number
    product_name = product_view.product.name

    for sale_product in sales_products_info:
        if product_name == sale_product['product']:
            price_in_sale = (product_view.product.price * (100 - int(sale_product['discount_percentage']))) // 100

            start_time, end_time = beautiful_datetime(sale_product['start_time'], sale_product['end_time'])

            text = f"Diqqat! Faqat {start_time} dan, {end_time} sanasigacha: " \
                   f"{str(product_name).capitalize()}ga -{sale_product['discount_percentage']}% chegirma, " \
                   f"chegirmadagi narx: {price_in_sale} so'm"

            phone_number_and_text.update({'phone_number': phone_number, 'text': text})
            break

    # return Response({'message': phone_number_and_text})
    return send_sms(phone_number_and_text)


def beautiful_datetime(time1, time2):
    dt = datetime.fromisoformat(str(time1))
    new_start_time = dt.strftime("%d/%m/%Y %H:%M")

    dt = datetime.fromisoformat(str(time2))
    new_end_time = dt.strftime("%d/%m/%Y %H:%M")

    return new_start_time, new_end_time


def send_sms(data):
    url = 'https://4e29v1.api.infobip.com/sms/2/text/advanced'
    headers = {'Authorization': f'App {SMS_KEY}', 'Content-Type': 'application/json', 'Accept': 'application/json'}

    payload = {
        'messages': [
            {
                'from': 'ChoyxonaExpress',
                'destinations': [{'to': str(data['phone_number']).replace('+', '')}],
                'text': data['text']
            }
        ]
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return Response({'message': 'SMS sent successfully'}, status=status.HTTP_200_OK)

    return Response({'message': 'Failed to sent SMS'}, status=status.HTTP_400_BAD_REQUEST)
