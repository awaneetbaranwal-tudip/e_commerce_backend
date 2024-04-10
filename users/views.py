from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from users.models import Address
from .serializers import AddressSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from base.utilities import Utilities
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

User = get_user_model()

class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
                'username':openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password','username']
        ),
        responses={}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"User registered successful")
        return Response(serializer.data)

class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            },
            required=['email', 'password']
        ),
        responses={}
    )
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    
@api_view(['GET'])
def user_list(request):
    try:
        user = Utilities.get_user(request)
        if not (user.is_staff or user.is_superuser):
            raise AuthenticationFailed('Only admin and staff can do this operation!')
        if request.method == 'GET':
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

address_schema = {
    "address_type": openapi.Schema(type=openapi.TYPE_STRING, enum=["B", "S"]),
    "default": openapi.Schema(type=openapi.TYPE_BOOLEAN),
    "country": openapi.Schema(type=openapi.TYPE_STRING),
    "city": openapi.Schema(type=openapi.TYPE_STRING),
    "street_address": openapi.Schema(type=openapi.TYPE_STRING),
    "apartment_address": openapi.Schema(type=openapi.TYPE_STRING),
    "postal_code": openapi.Schema(type=openapi.TYPE_STRING),
    "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
}
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=address_schema,
        required=['user', 'address_type', 'country', 'city', 'street_address']
    )
)
@api_view(['GET', 'POST'])
def address_list(request):
    try:
        if request.method == 'GET':
            addresses = Address.objects.all()
            serializer = AddressSerializer(addresses, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            user = Utilities.get_user(request)
            request.data['user']=user.id
            request.data['created_by']=user.id
            serializer = AddressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Address created successful")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

address_schema = {
    "address_type": openapi.Schema(type=openapi.TYPE_STRING, enum=["B", "S"]),
    "default": openapi.Schema(type=openapi.TYPE_BOOLEAN),
    "country": openapi.Schema(type=openapi.TYPE_STRING),
    "city": openapi.Schema(type=openapi.TYPE_STRING),
    "street_address": openapi.Schema(type=openapi.TYPE_STRING),
    "apartment_address": openapi.Schema(type=openapi.TYPE_STRING),
    "postal_code": openapi.Schema(type=openapi.TYPE_STRING),
    "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
}
@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=address_schema,
        required=['user', 'address_type', 'country', 'city', 'street_address']
    )
)
@api_view(['GET', 'PUT', 'DELETE'])
def address_detail(request, pk):
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Address updated successful")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        address.delete()
        logger.info("Address deleted successful")
        return Response(status=status.HTTP_204_NO_CONTENT)
    

