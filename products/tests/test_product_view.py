from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from products.models import ProductViewHistory, Product, Category

User = get_user_model()


class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(phone_number='+998974684512', password='testuser1')
        self.user2 = User.objects.create(phone_number='+998976543696', password='testuser2')
        self.staff_user = User.objects.create(phone_number='+998993014587', password='teststaff', is_staff=True)

        self.category1 = Category.objects.create(name='Books')

        self.product1 = Product.objects.create(category=self.category1, name='Xamsa', description='Xamsa kitobi', price=400_000, stock=25)

        self.productview1 = ProductViewHistory.objects.create(user=self.user1, product=self.product1)
        # self.productview2 = ProductViewHistory.objects.create(user=self.user, product=self.product1)

    def test_product_view_history_list(self):
        url = reverse('product-view-history-list-create')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_permission_denied_product_view_history_create_for_regular_user(self):
        url = reverse('product-view-history-list-create')
        self.client.force_authenticate(user=self.user2)
        data = {
            'user': self.user2.pk,
            'product': self.product1.pk
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_granted_product_view_history_create_for_staff_user(self):
        url = reverse('product-view-history-list-create')
        self.client.force_authenticate(user=self.staff_user)
        data = {
            'user': self.staff_user.pk,
            'product': self.product1.pk
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductViewHistory.objects.count(), 2)
