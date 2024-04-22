import json
import random
import string
import jwt
from django.conf import settings
from datetime import datetime, timedelta

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import BasePermission

from .serializers import UserSerializer, BanSerializer
from .models import User, VerifyCode, Ban


# 自定义认证方法
# 自定义权限方法
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


class SendVerifyCode(APIView):
    authentication_classes = []

    def post(self, request):
        phone_number = request.POST.get('phone')
        find_number = User.objects.filter(phone=phone_number).first()
        find_code = VerifyCode.objects.filter(phone=phone_number).first()
        if find_number:
            # 如果该手机号码已存在用户，则返回错误响应
            return Response({'code': 1, 'message': '此电话号码已存在，不要重复注册'})

        else:
            code = ''.join(random.choices('0123456789', k=6))
            print(code)
            if find_code:
                # 如果该手机号码已存在验证码，则返回错误响应
                find_code.code = code
                find_code.save()
            else:
                # 如果该手机号码不存在验证码，则生成验证码并存入数据库
                VerifyCode.objects.create(phone=phone_number, code=code)

            # 返回成功响应
            return Response({'code': 0, 'message': '验证码发送成功'})


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        # 获取请求体中的数据
        data = json.loads(request.body)
        phone_number = data.get('phone')
        password = data.get('password')
        find_user = User.objects.filter(phone=phone_number, password=password).first()
        user_id = find_user.id
        user_name = find_user.name
        if not find_user:
            # 如果用户不存在或密码错误，返回错误响应
            return Response({'code': 1, 'message': '用户不存在或密码错误'})
        salt = settings.SECRET_KEY
        payload = {
            'user_id': user_id,
            'name': user_name,
            'role': find_user.role,
            'exp': datetime.utcnow() + timedelta(minutes=15)
        }
        token = jwt.encode(payload=payload, key=salt, algorithm='HS256')
        # 如果用户存在且密码正确，则返回成功响应
        return Response(
            {'code': 0, 'message': '登录成功', 'user_phone': find_user.phone, "user_name": user_name,
             "token": token})


class RegisterView(APIView):
    authentication_classes = []

    def post(self, request):
        # 获取请求体中的数据
        phone_number = request.data.get('phone')
        code = request.data.get('code')
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 验证验证码
        find_code = VerifyCode.objects.filter(phone=phone_number, code=code).first()
        if not find_code:
            # 如果验证码错误，返回错误响应
            return Response({'code': 1, 'message': '验证码错误'})

        # 如果验证码正确，则创建用户并返回成功响应
        # 此处省略了用户创建代码
        def generate_random_string(length):
            characters = string.ascii_letters + string.digits
            return ''.join(random.choice(characters) for i in range(length))

        name = generate_random_string(8)
        data = request.data
        data['name'] = name
        data['time'] = time
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            # 如果数据有效，保存到数据库
            serializer.save()
            return Response({'code': 0, 'message': '用户创建成功'})
        else:
            # 如果数据无效，返回错误响应
            return Response({'code': 1, 'message': '用户创建失败', 'errors': serializer.errors})


class UserInfoView(APIView):
    permission_classes = [UserPermission]

    # 获取用户列表
    def get(self, request):
        page = int(request.GET.get('page'))
        users = User.objects.all().order_by('time')[(page - 1) * 10:page * 10]
        count = User.objects.all().count()
        print(count)
        serializer = UserSerializer(users, many=True)

        return Response({'code': 0, 'data': serializer.data, 'count': count})

    # 设置管理员
    def patch(self, request):
        data = request.data
        phone = data.get('phone')
        User.objects.filter(name=phone).update(stateCode="2", role="admin")
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time)
        return Response({'code': 0, 'message': '用户已设置为管理员'})

    # 取消管理员
    def post(self, request):
        phone = request.data.get('phone')
        User.objects.filter(name=phone).update(stateCode="0", role="user")
        return JsonResponse({'code': 0, 'message': '用户已设置为普通用户'})


class BanlistView(APIView):
    # 获取被禁用户列表
    def get(self, request):
        page = int(request.GET.get('page'))
        bans = Ban.objects.all().order_by('time')[(page - 1) * 10:page * 10]
        count = Ban.objects.all().count()
        print("bancount:", count)
        serializer = BanSerializer(bans, many=True)
        return Response({'code': 0, 'data': serializer.data, 'count': count})

    # 封禁用户
    def post(self, request):
        phone = request.data.get('phone')
        print(phone)
        User.objects.filter(phone=phone).update(stateCode="1")
        name = User.objects.filter(phone=phone).first().name
        Ban.objects.create(phone=phone, name=name, reason=request.data.get('reason'),
                           time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return Response({'code': 0, 'message': '用户已被封禁'})

    # 解除封禁
    def delete(self, request):
        phone = request.GET.get('phone')
        User.objects.filter(phone=phone).update(stateCode="0")
        Ban.objects.filter(phone=phone).delete()
        return Response({'code': 0, 'message': '封禁已解除'})


class SearchView(APIView):
    def get(self, request):
        name = request.GET.get('name')
        users = User.objects.filter(name=name)
        count = users.count()
        print("usercount:", count)
        serializer = UserSerializer(users, many=True)
        return Response({'code': 0, 'data': serializer.data, "count": count})
