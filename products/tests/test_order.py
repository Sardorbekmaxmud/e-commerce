from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.db.models.signals import post_save
from products.signals import notify_admin
from django.conf import settings

from products.models import Order, Product, Category

User = get_user_model()


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        # Signalni vaqtincha o‘chirib qo‘yamiz
        post_save.disconnect(receiver=notify_admin, sender=Order)

        self.user1 = User.objects.create(phone_number='+998911234567', password='testtest', email=settings.EMAIL_HOST_USER, username='Testuser1')
        self.user2 = User.objects.create(phone_number='+998933133336', password='passpass', email=settings.OTHER_USER_EMAIL, username='Testuser2')

        self.category1 = Category.objects.create(name='Books')

        self.product1 = Product.objects.create(category=self.category1, name="Raqamli qal'a", description='Den Braun qalamiga mansub kitob. Dasturlash va kriptografiya haqida.', price=45_000, stock=120)
        self.product2 = Product.objects.create(category=self.category1, name="Diqqat", description='Kel Nyuport qalamiga mansub, hozirgi zamonda diqqatni yig\'ish haqida.', price=63_000, stock=15)
        self.product3 = Product.objects.create(category=self.category1, name="Mehrobdan chayon", description='Abdulla Qodiriy qalamiga mansub, 19 asrdagi hayot tasvirlangan.', price=52_000, stock=50)

        self.order1 = Order.objects.create(product=self.product1, customer=self.user1, quantity=1, phone_number='+998881547755')
        self.order2 = Order.objects.create(product=self.product2, customer=self.user2, quantity=5, phone_number='+998942230321')
        self.order3 = Order.objects.create(product=self.product3, customer=self.user2, quantity=3, phone_number='+998942230321')
        self.order4 = Order.objects.create(product=self.product1, customer=self.user1, quantity=10, phone_number='+998994556556')

    def tearDown(self):
        # Signalni qayta ulaymiz
        post_save.connect(receiver=notify_admin, sender=Order)

    def test_order_list(self):
        url = reverse('order-list')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)

    def test_order_detail(self):
        url = reverse('order-detail', args=[self.order4.pk])
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 10)

    def test_order_create(self):
        url = reverse('order-list')
        self.client.force_authenticate(user=self.user1)
        data = {'product': 2, 'customer': 1, 'quantity': 1, 'phone_number': '+998916213545'}
        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(first=response.status_code, second=status.HTTP_201_CREATED)
        self.assertEqual(first=Order.objects.count(), second=5)

    def test_order_update(self):
        url = reverse('order-detail', args=[self.order1.pk])
        self.client.force_authenticate(user=self.user1)
        data = {'status': 'CANCELED'}
        response = self.client.patch(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.order1.refresh_from_db()
        self.assertEqual(self.order1.status, 'CANCELED')

    def test_order_delete(self):
        url = reverse('order-detail', args=[self.order2.pk])
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permission_denied_for_not_owner(self):
        url = reverse('order-detail', args=[self.order3.pk])
        self.client.force_authenticate(user=self.user1)
        data = {'status': 'CANCELED'}
        response = self.client.patch(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
