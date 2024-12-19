from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from products.models import Product

# Create your models here.
phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqam quyidagi shaklda bo'lishi kerak: '+998xxxxxxxxx'"
)


class Order(models.Model):
    PENDING = 'Pending'  # Ko'rib chiqilyapti
    PROCESSING = 'Processing'  # Yig'ilyapti
    SHIPPED = 'Shipped'  # Yuklandi
    DELIVERED = 'Delivered'  # Xarirdorga yetkazildi
    CANCELED = 'Canceled'  # Bekor qilindi

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELED', 'Canceled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING,)
    phone_number = models.CharField(max_length=13, validators=[phone_regex])

    def set_status(self, new_status) -> None:
        """
        Order statusini STATUS_CHOICES da bor bo'lsa,
        new_status ga o'zgartirib beradi.
        """
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError('Invalid status')

        self.status = new_status
        self.save()

    def is_transition_allowed(self, new_status) -> bool:
        """
        Orderni statusini ketma-ket ravishda to'g'ri holatda
        o'zgartirilishini taminlab beradi.
        """
        allowed_transitions = {
            self.PENDING: [self.PROCESSING, self.CANCELED],
            self.PROCESSING: [self.SHIPPED, self.CANCELED],
            self.SHIPPED: [self.DELIVERED, self.CANCELED]
        }
        return new_status in allowed_transitions.get(self.status, [])

    def __str__(self) -> str:
        return f"Order({self.product.name}) by {self.customer.username}"
