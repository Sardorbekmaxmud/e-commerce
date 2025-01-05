from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from products.models import Product


User = get_user_model()


# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.PositiveSmallIntegerField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.user} - {self.product.name} - {self.rating}"


class FlashSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    class Meta:
        unique_together = ['product', 'start_time', 'end_time']
        ordering = ['-id']


class ProductViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "product view histories"
        ordering = ['id']

    def __repr__(self):
        return f"{self.user.phone_number} {self.product.name}"
