from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.models import Products
from .serializers import ProductSerializer, CategorySerializer
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from base.utilities import Utilities

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

schema = {
    "seller": openapi.Schema(type=openapi.TYPE_STRING),
    "category": openapi.Schema(type=openapi.TYPE_INTEGER),
    "name": openapi.Schema(type=openapi.TYPE_STRING),
    "desc": openapi.Schema(type=openapi.TYPE_STRING),
    "price": openapi.Schema(type=openapi.TYPE_NUMBER),
    "quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
}
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=schema,
    required=['seller','category','name','desc','price','quantity']
))
@api_view(['POST'])
def add_product(request):
    user = Utilities.get_user(request)
    if not (user.is_staff or user.is_superuser):
            raise AuthenticationFailed('Only admin and staff can do this operation!')
    request.data['created_by'] = user.id
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_product(request, pk):
    try:
        products = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(products)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_products(request):
    try:
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_product(request, pk):
    user = Utilities.get_user(request)
    if not (user.is_staff or user.is_superuser):
            raise AuthenticationFailed('Only admin and staff can do this operation!')
    try:
        product = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    request.data['modified_by'] = user.id
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()                                                                                                                                                                                                                                                          
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_product(request, pk):
    user = Utilities.get_user(request)
    if not (user.is_staff or user.is_superuser):
            raise AuthenticationFailed('Only admin and staff can do this operation!')
    try:
        products = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    products.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

schema = {
    "name": openapi.Schema(type=openapi.TYPE_STRING),
    "description": openapi.Schema(type=openapi.TYPE_STRING)
}
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=schema,
    required=['name','description']
))
@api_view(['POST'])
def add_category(request):
    user = Utilities.get_user(request)
    if not (user.is_staff or user.is_superuser):
            raise AuthenticationFailed('Only admin and staff can do this operation!')
    request.data['created_by'] = user.id
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
