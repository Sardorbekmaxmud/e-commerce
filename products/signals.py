from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
import requests

from .models import Order


@receiver(post_save, sender=Order)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        token = settings.TELEGRAM_BOT_TOKEN
        admin_id = settings.ADMIN_ID
        method = 'sendMessage'

        message_text = f"New Order: {instance.id}\nProduct: {instance.product.name}\n" \
                       f"Quantity: {instance.quantity}\nClient: {instance.customer.username}\n" \
                       f"Phone: {instance.phone_number}\nCreated: {instance.created_at}"
        response = requests.post(
            url=f'https://api.telegram.org/bot{token}/{method}',
            data={'chat_id': admin_id, 'text': message_text}
        ).json()
