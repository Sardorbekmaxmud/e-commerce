from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from products.models import Category

User = get_user_model()


class CategoryViewSetTestCase(APITestCase):
    fixtures = ['categories']

    def setUp(self):
        self.user = User.objects.create(phone_number='+998333030303', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.category1 = Category.objects.first()

    def test_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)

    def test_category_detail(self):
        url = reverse('category-detail', args=[4])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Drinks')

    def test_category_create(self):
        url = reverse('category-list')
        data = {'name': 'Cars'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_update(self):
        url = reverse('category-detail', args=[self.category1.pk])
        data = {'name': 'Vehicles'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'Vehicles')

    def test_category_delete(self):
        url = reverse('category-detail', args=[self.category1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permission_denied_for_anonymous_user(self):
        url = reverse('category-list')
        self.client.force_authenticate(user=None)
        data = {'name': 'Lavash'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_granted_for_logged_user(self):
        url = reverse('category-list')
        data = {'name': 'Lavash'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 7)
