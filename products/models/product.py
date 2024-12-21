from django.db import models


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
    stock = models.IntegerField(default=0)

    def is_in_stock(self) -> bool:
        return self.stock > 0

    def reduce_stock(self, quantity) -> bool:
        if quantity > self.stock:
            return False
        self.stock -= quantity
        self.save()

    def increase_stock(self, amount) -> None:
        if amount <= 0:
            raise False
        self.stock += amount
        self.save()

    def __str__(self):
        return self.name
