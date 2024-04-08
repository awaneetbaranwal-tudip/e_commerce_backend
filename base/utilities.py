from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.contrib.auth import get_user_model

User = get_user_model()

class Utilities:
    @staticmethod
    def get_user(request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithm='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        return user


# def getUser(self, request):
#     token = request.COOKIES.get('jwt')
#     if not token:
#         raise AuthenticationFailed('Unauthenticated!')
#     try:
#         payload = jwt.decode(token, 'secret', algorithm=['HS256'])
#     except jwt.ExpiredSignatureError:
#         raise AuthenticationFailed('Unauthenticated!')

#     user = User.objects.filter(id=payload['id']).first()
#     return user