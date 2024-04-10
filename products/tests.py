from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category,Products
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from .models import Category
from datetime import datetime,timedelta
import jwt

class ProductTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', description='Test Description')
        self.regular_user = User.objects.create_user(username='user', password='user_pass')
        self.admin_user = User.objects.create_user(username='admin', password='admin_pass', is_staff=True, is_superuser=True)
        self.product = Products.objects.create(name='Test Product', desc='Test Description', price=10.0, quantity=5, category=self.category , seller=self.regular_user)
    
    def test_get_all_products(self):
        url = reverse('get_all_products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_product_admin_user(self):
        # Generate JWT token for regular user
        token = self.generate_token(self.admin_user)
        self.client.cookies['jwt'] = token

        request_data = {'seller':self.regular_user.id,'category':self.category.id,'price':100,'quantity':100,'name': 'test1', 'desc': 'test prod'}
        response = self.client.post(reverse('add_product'), data=request_data) 

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def generate_token(self, user):
        payload = {
            'id': user.id,
            'exp':  datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        return token

class CategoryTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='admin_pass', is_staff=True, is_superuser=True)
        self.staff_user = User.objects.create_user(username='staff', password='staff_pass', is_staff=True)
        self.regular_user = User.objects.create_user(username='user', password='user_pass')

    def test_get_all_categories(self):
        url = reverse('get_all_categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_category_admin_user(self):
        # Generate JWT token for regular user
        token = self.generate_token(self.admin_user)
        self.client.cookies['jwt'] = token
        # Make request with regular user token
        request_data = {'name': 'Test Category', 'description': 'Test Description'}
        response = self.client.post(reverse('add_category'), data=request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_category_staff_user(self):
        # Generate JWT token for regular user
        token = self.generate_token(self.staff_user)
        self.client.cookies['jwt'] = token
        # Make request with regular user token
        request_data = {'name': 'Test Category', 'description': 'Test Description'}
        response = self.client.post(reverse('add_category'), data=request_data)
        # Check if user gets AuthenticationFailed error
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_category_regular_user(self):
        # Generate JWT token for regular user
        token = self.generate_token(self.regular_user)
        self.client.cookies['jwt'] = token
        # Make request with regular user token
        request_data = {'name': 'Test Category', 'description': 'Test Description'}
        response = self.client.post(reverse('add_category'), data=request_data)

        # Check if user gets AuthenticationFailed error
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def generate_token(self, user):
        payload = {
            'id': user.id,
            'exp':  datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        return token

