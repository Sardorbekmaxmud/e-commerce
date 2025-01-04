from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from products.models import Review, Product, Category

User = get_user_model()


class ReviewViewSetTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(phone_number='+998202002020', password='testqwerty')
        self.user2 = User.objects.create(phone_number='+998202012121', password='testpass')

        self.category1 = Category.objects.create(name='Electronics')

        self.product1 = Product.objects.create(category=self.category1, name='Asus Gaming Laptop', description='Gaming laptop', price=9_500_000, stock=20)

        self.review1 = Review.objects.create(user=self.user1, product=self.product1, content='This laptop is so great to playing games', rating=5)
        self.review2 = Review.objects.create(user=self.user2, product=self.product1, content='Noutbuk yaxshi holatda emas. Qotip, pirmirap qolyapti.', rating=3)

    def test_review_list(self):
        url = reverse('review-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_review_detail(self):
        url = reverse('review-detail', args=[self.review1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'This laptop is so great to playing games')

    def test_review_create(self):
        url = reverse('review-list')
        data = {'user': 2, 'product': 1, 'content': 'Noutbuk yaxshi holatda, faqat yaxshilab windows qilib bermapdilar', 'rating': 4}
        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 3)

    def test_review_update(self):
        url = reverse('review-detail', args=[self.review2.pk])
        data = {'content': 'Noutbukni almashtirib berishdi. Endi hammasi ajoyib.'}
        response = self.client.patch(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.review2.refresh_from_db()
        self.assertEqual(self.review2.content, 'Noutbukni almashtirib berishdi. Endi hammasi ajoyib.')

    def test_review_delete(self):
        url = reverse('review-detail', args=[self.review2.pk])
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


