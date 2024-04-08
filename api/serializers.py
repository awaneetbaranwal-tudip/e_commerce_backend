from rest_framework import serializers
from products.models import Products, Category
from orders.models import Orders
from users_cart.models import UserCart
from django.contrib.auth import get_user_model
from users.models import Address
User = get_user_model()



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



# class ProfileSerializer(serializers.ModelSerializer):
#     """
#     Serializer class to serialize the user Profile model
#     """

#     class Meta:
#         model = Profile
#         fields = (
#             "bio",
#             "created_at",
#             "updated_at",
#         )