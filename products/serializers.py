from rest_framework import serializers
from products.models import Products, Category
from django.contrib.auth import get_user_model
User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'