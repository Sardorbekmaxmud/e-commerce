from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from django.utils import timezone

from products.models import FlashSale, Product, Category, ProductViewHistory

User = get_user_model()


class FlashSaleViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(phone_number='+998945821145', password='testuser')
        self.staff_user = User.objects.create(phone_number='+998978945885', password='teststaffuser', is_staff=True)

        self.category1 = Category.objects.create(name='Telefonlar')
        self.category2 = Category.objects.create(name='Oshxona buyumlari')

        self.product1 = Product.objects.create(category=self.category1, name='Samsung S24', description='Zamonaviy, qulay telefon', price=8_500_000, stock=25)
        self.product2 = Product.objects.create(category=self.category2, name='Shivaki qozoni', description='Zamonaviy qozon', price=225_000, stock=50)

        today = timezone.now().date()
        start_time1 = timezone.make_aware(datetime.combine(today, datetime.min.time()) + timedelta(hours=8))
        end_time1 = timezone.make_aware(datetime.combine((timezone.now() + timedelta(days=3)).date(), datetime.min.time()) + timedelta(hours=17, minutes=59, seconds=59))

        start_time2 = timezone.make_aware(datetime.combine((timezone.now() + timedelta(days=7)).date(), datetime.min.time()) + timedelta(hours=8, minutes=0, seconds=0))
        end_time2 = timezone.make_aware(datetime.combine((timezone.now() + timedelta(days=10)).date(), datetime.min.time()) + timedelta(hours=17, minutes=59, seconds=59))

        self.flash_sale1 = FlashSale.objects.create(product=self.product1, discount_percentage=10, start_time=start_time1, end_time=end_time1)
        self.flash_sale2 = FlashSale.objects.create(product=self.product2, discount_percentage=15, start_time=start_time2, end_time=end_time2)

        self.productview1 = ProductViewHistory.objects.create(user=self.user, product=self.product1)

    def test_flash_sale_list(self):
        url = reverse('sale')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_permission_denied_for_regular_user_flash_sale_create(self):
        url = reverse('sale')
        self.client.force_authenticate(user=self.user)

        start_time = timezone.make_aware(datetime(2025, 1, 17, 8, 0, 0))
        end_time = timezone.make_aware(datetime(2025, 1, 20, 18, 0, 0))
        data = {
            'product': 'Samsung S24',
            'discount_percentage': 50,
            'start_time': start_time,
            'end_time': end_time
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_granted_for_staff_user_flash_sale_create(self):
        url = reverse('sale')
        self.client.force_authenticate(user=self.staff_user)

        start_time = timezone.make_aware(datetime(year=2025, month=1, day=17, hour=8, minute=0, second=0))
        end_time = timezone.make_aware(datetime(year=2025, month=1, day=20, hour=18, minute=0, second=0))
        data = {
            'product': self.product1.pk,
            'discount_percentage': 5,
            'start_time': start_time,
            'end_time': end_time
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FlashSale.objects.count(), 3)

    def test_check_flesh_sale_detail(self):
        url = reverse('check-sale', args=[self.product1.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
