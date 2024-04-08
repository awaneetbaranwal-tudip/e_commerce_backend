from rest_framework import serializers
from users_cart.models import UserCart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        fields = '__all__'