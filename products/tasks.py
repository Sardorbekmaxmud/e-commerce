from django.conf import settings
from celery import shared_task
import requests
import time


@shared_task  # Celery async tarzda avtomatik bajaradi.
def send_telegram_notification(order_id, product_name, quantity, customer_phone_number, phone_number, created_at, status, is_paid):
    time.sleep(5)

    token = settings.TELEGRAM_BOT_TOKEN
    admin_id = settings.ADMIN_ID
    method = 'sendMessage'

    message_text = f"New Order: {order_id}\nProduct: {product_name}\n" \
                   f"Quantity: {quantity}\nClient: {customer_phone_number}\n" \
                   f"Phone: {phone_number}\nCreated: {created_at}\n" \
                   f"Status: {status}\nPaid: {is_paid}"
    response = requests.post(
        url=f'https://api.telegram.org/bot{token}/{method}',
        data={'chat_id': admin_id, 'text': message_text}
    ).json()
