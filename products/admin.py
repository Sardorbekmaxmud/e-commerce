from django.contrib import admin
from products.models import (Category, Product, Review,
                             ProductViewHistory, FlashSale,
                             Order)

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ProductViewHistory)
admin.site.register(FlashSale)
admin.site.register(Order)
