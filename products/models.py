from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.PositiveSmallIntegerField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product.name} - {self.rating}"
