from django.urls import reverse
from rest_framework.test import APITestCase
from products.models import Category, Product, Review
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(phone_number='+998998765432', password='testroot')
        self.staff_user = User.objects.create(phone_number='+998912345678', password='teststaffroot', is_staff=True)

        self.category1 = Category.objects.create(name='Pozabzallar')
        self.category2 = Category.objects.create(name='Ichimliklar')

        self.product1 = Product.objects.create(category=self.category1, name='Krassofka', description="42 o'lchamli. Adidas kompaniya mahsuloti", stock=100, price=250_000)
        self.product2 = Product.objects.create(category=self.category2, name='Dinay', description="1.5l nok sharbati", stock=50, price=12_000)

        Review.objects.create(user=self.user, product=self.product1,content="Krassofka zo'r ekan. Hammaga tavsiya qilaman.", rating=5)
        Review.objects.create(user=self.staff_user, product=self.product2, content="Mazali nok sharbati ekan.",rating=5)
        Review.objects.create(user=self.user, product=self.product1,content="Krassofkaning o'lchami to'gri kelmadi. 2 o'lcham kattaroq olinglar.", rating=3)

    def test_product_list(self):
        url = reverse('product-list')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_product_filter_by_category(self):
        url = reverse('product-list') + "?category=" + str(self.category1.id)
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(first=len(response.data['results']), second=1)

    def test_product_detail(self):
        url = reverse('product-detail', args=[self.product1.id])
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product']['name'], 'Krassofka')

    def test_product_rating(self):
        url = reverse('product-top-rating')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.product2.name)  # Dinay

    def test_product_average_rating(self):
        url = reverse('product-average-rating', args=[self.product1.id])
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.data['average_rating'], 4.0)

    def test_product_create(self):
        url = reverse('product-list')
        self.client.force_authenticate(self.staff_user)
        data = {'category': 2, 'name': "1.0l Milliy cola", 'description': "O'zimizning milliy cola. 1.0l", 'price': 8_000, 'stock': 1_000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product2.refresh_from_db()
        self.assertEqual(Product.objects.count(), 3)

    def test_product_update(self):
        url = reverse('product-detail', args=[self.product2.pk])
        self.client.force_authenticate(user=self.staff_user)
        data = {'name': 'Dinay nok', 'description': '1.0l nok sharbati'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product2.refresh_from_db()
        self.assertEqual(self.product2.name, 'Dinay nok')

    def test_product_delete(self):
        url = reverse('product-detail', args=[self.product2.pk])
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)

    def test_permission_denied_for_anonymous_user(self):
        url = reverse('product-list')
        self.client.force_authenticate(user=None)
        data = {'category': 2, 'name': '1.0l DaDa apelsin', 'description': '1.0l Dada apelsin sharbati', 'price': 10_000, 'stock': 50}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_granted_for_staff_user(self):
        url = reverse('product-list')
        self.client.force_authenticate(user=self.staff_user)
        data = {'category': 2, 'name': '1.0l DaDa apelsin', 'description': '1.0l Dada apelsin sharbati', 'price': 10_000, 'stock': 50}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_permission_for_staff_user_update_admin_product_replenish_stock(self):
        url = reverse('admin-replenish-stock', args=[self.product1.pk, 50])
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.put(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, 150)

    def test_permission_for_regular_user_update_admin_product_replenish_stock(self):
        url = reverse('admin-replenish-stock', args=[self.product1.pk, 50])
        self.client.force_authenticate(user=self.user)
        response = self.client.put(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
