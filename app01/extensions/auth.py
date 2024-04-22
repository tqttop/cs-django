from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from jwt import exceptions
import jwt


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        salt = settings.SECRET_KEY
        try:
            payload = jwt.decode(token, salt, algorithms=['HS256'])
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code': 1, 'message': 'Token过期，请重新登录'})
        except exceptions.DecodeError:
            raise AuthenticationFailed({'code': 1, 'message': 'Token认证失败，请重新登录'})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code': 1, 'message': 'Token非法，请重新登录'})
        return payload, token
