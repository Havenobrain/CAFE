from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order

class OrderAPITestCase(TestCase):
    def setUp(self):
        """Настройка тестового окружения"""
        self.client = APIClient()
        self.order = Order.objects.create(
            table_number=1,
            items="Суп - 100\nЧай - 50",
            status="pending",
            total_price=150
        )

    def test_get_orders(self):
        """Проверка получения всех заказов"""
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_order_by_id(self):
        """Проверка получения заказа по ID"""
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.id)

    def test_create_order(self):
        """Проверка создания заказа"""
        data = {
            "table_number": 2,
            "items": "Пицца - 200\nСок - 100",
            "status": "pending"
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['table_number'], 2)

    def test_update_order(self):
        """Проверка обновления заказа"""
        data = {
            "table_number": 1,
            "items": "Суп - 120\nКофе - 70",
            "status": "ready"
        }
        response = self.client.put(f'/api/orders/{self.order.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "ready")

    def test_delete_order(self):
        """Проверка удаления заказа"""
        response = self.client.delete(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_create_order(self):
        """Проверка создания заказа с некорректными данными"""
        data = {
            "table_number": -1,
            "items": "",
            "status": "unknown"
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('table_number', response.data)
        self.assertIn('items', response.data)
        self.assertIn('status', response.data)
