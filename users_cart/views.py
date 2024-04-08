from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.models import Products
from .serializers import CartSerializer
from rest_framework import status
from users_cart.models import UserCart
from django.http import JsonResponse
from base.utilities import Utilities
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from base.utilities import Utilities

schema = {
    "product": openapi.Schema(type=openapi.TYPE_INTEGER),
    "quantity": openapi.Schema(type=openapi.TYPE_INTEGER),

}
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=schema,
    required=['product','quantity']
))
@api_view(['POST'])
def add_product_to_cart(request):
    product_id = request.data.get('product')
    quantity = request.data.get('quantity', 1)
    print(f"product_id is {product_id}")
    try:
        product = Products.objects.get(pk=product_id)
    except Products.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if product.quantity < quantity:
        return JsonResponse({'error': f"Not enough quantity available for {product.name}"}, status=status.HTTP_400_BAD_REQUEST)
    user = Utilities.get_user(request)
    
    # Check if the product is already in the user's cart
    try:
        cart_item = UserCart.objects.get(user=user, product=product)
        cart_item.quantity += quantity 
        cart_item.save()
        serializer = CartSerializer(cart_item)
        return Response(serializer.data)
    except UserCart.DoesNotExist:
        pass
    
    request.data['created_by'] = user.id
    request.data['price'] = product.price
    request.data['user'] = user.id
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_products_from_cart(request):
    user = Utilities.get_user(request)
    products = UserCart.objects.filter(user=user)
    serializer = CartSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def update_cart_product(request, pk):
    try:
        cart_item = UserCart.objects.get(pk=pk, user=request.user)
    except UserCart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CartSerializer(cart_item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_cart_product(request, pk):
    try:
        cart_item = UserCart.objects.get(pk=pk, user=request.user)
    except UserCart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    cart_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
