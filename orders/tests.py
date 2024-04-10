from django.test import TestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from users_cart.models import UserCart
from orders.models import Orders
from order_items.models import OrderItems
from datetime import datetime,timedelta
from products.models import Category,Products
import jwt

class PlaceOrderTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.category = Category.objects.create(name='Test Category', description='Test Description')
        self.seller_user = User.objects.create_user(username='user_seller', password='user_pass')
        self.buyer_user = User.objects.create_user(username='user_buyer', password='user_pass')
        self.admin_user = User.objects.create_user(username='admin', password='admin_pass', is_staff=True, is_superuser=True)
        self.product1 = Products.objects.create(name='Test Product1', desc='Test Description1', price=10.0, quantity=15, category=self.category , seller=self.seller_user)
        self.product2 = Products.objects.create(name='Test Product2', desc='Test Description2', price=105.0, quantity=30, category=self.category , seller=self.seller_user)

        self.cart_item1 = UserCart.objects.create(user=self.buyer_user, product_id=self.product1.id, quantity=2, price=self.product1.price)
        self.cart_item1 = UserCart.objects.create(user=self.buyer_user, product_id=self.product2.id, quantity=3, price=self.product2.price)

    def test_place_order(self):
        # Get the initial count of orders

        token = self.generate_token(self.buyer_user)
        self.client.cookies['jwt'] = token

        initial_order_count = Orders.objects.count()
        # Make a POST request to place an order
        url = reverse('order')
        response = self.client.post(url)
        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the order was created
        self.assertEqual(Orders.objects.count(), initial_order_count + 1)
        # Check if cart items were deleted
        self.assertFalse(UserCart.objects.filter(user=self.buyer_user).exists())
        # Check if order items were created
        self.assertEqual(OrderItems.objects.filter(orders=response.data['order_id']).count(), 2)

    def generate_token(self, user):
        payload = {
            'id': user.id,
            'exp':  datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        return token
