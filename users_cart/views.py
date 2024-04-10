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
from rest_framework.exceptions import NotFound
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

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
        logger.info(f"Quantity increased by {quantity}")
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
        logger.info(f"Product added in cart")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_products_from_cart(request):
    try:
        user = Utilities.get_user(request)
        products = UserCart.objects.filter(user=user)
        if not products:
            raise NotFound("No products found in the user's cart")
        
        serializer = CartSerializer(products, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


schema = {
    "product": openapi.Schema(type=openapi.TYPE_INTEGER),
    "quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
}
@swagger_auto_schema(method='put', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=schema,
    required=['product','quantity']
))
@api_view(['PUT'])
def update_cart_product(request, pk):
    try:
        user = Utilities.get_user(request)
        
        cart_item = UserCart.objects.get(pk=pk, user=user)
        
        request.data['user'] = user.id
        request.data['modified_by'] = user.id
        serializer = CartSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Cart updated successful")
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except UserCart.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_cart_product(request, pk):
    try:
        user = Utilities.get_user(request)
        cart_item = UserCart.objects.get(pk=pk, user=user)
    except UserCart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    cart_item.delete()
    message = f"Cart product deleted"
    logger.info(message)
    return Response(status=status.HTTP_204_NO_CONTENT)
