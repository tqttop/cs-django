from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from jwt import exceptions
import jwt
from rest_framework.permissions import BasePermission


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


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        permission_dict = settings.PERMISSIONS[request.user.get('role')]
        print("role:", request.user.get('role'))
        url_name = request.resolver_match.url_name
        method = request.method
        method_list = permission_dict.get(url_name)
        if not method_list:
            return False
        if method in method_list:
            return True
        return False
        # 验证用户是否登录

    def has_object_permission(self, request, view, obj):
        return True
