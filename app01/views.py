from django.shortcuts import render
import json
import string
from datetime import datetime
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import VerifyCode, User, Ban, Admin
import random
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def sendverifycode(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        find_number = User.objects.filter(phone=phone_number).first()
        find_code = VerifyCode.objects.filter(phone=phone_number).first()
        if find_number:
            # 如果该手机号码已存在用户，则返回错误响应
            return JsonResponse({'code': 1, 'message': '此电话号码已存在，不要重复注册'})

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
            return JsonResponse({'code': 0, 'message': '验证码发送成功'})
    else:
        # 如果请求方法不是 POST，返回错误响应
        return JsonResponse({'code': 1, 'message': 'Only POST requests are allowed.'})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 获取请求体中的数据
        data = json.loads(request.body)
        phone_number = data.get('phone')
        code = data.get('code')
        password = data.get('password')
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(phone_number, code, password, time)

        # 验证验证码
        find_code = VerifyCode.objects.filter(phone=phone_number, code=code).first()
        if not find_code:
            # 如果验证码错误，返回错误响应
            return JsonResponse({'code': 1, 'message': '验证码错误'})

        # 如果验证码正确，则创建用户并返回成功响应
        # 此处省略了用户创建代码
        def generate_random_string(length):
            characters = string.ascii_letters + string.digits
            return ''.join(random.choice(characters) for i in range(length))

        name = generate_random_string(8)
        User.objects.create(phone=phone_number, password=password, time=time, name=name)
        return JsonResponse({'code': 0, 'message': '用户创建成功'})
    else:
        # 如果请求方法不是 POST，返回错误响应
        return JsonResponse({'code': 1, 'message': 'Only POST requests are allowed.'})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 获取请求体中的数据
        data = json.loads(request.body)
        phone_number = data.get('phone')
        password = data.get('password')
        find_user = User.objects.filter(phone=phone_number, password=password).first()
        if not find_user:
            # 如果用户不存在或密码错误，返回错误响应
            return JsonResponse({'code': 1, 'message': '用户不存在或密码错误'})
        refresh = RefreshToken.for_user(find_user)
        # 如果用户存在且密码正确，则返回成功响应
        return JsonResponse(
            {'code': 0, 'message': '登录成功', 'user_phone': find_user.phone, "token": str(refresh)})


@csrf_exempt
def userlist(request):
    if request.method == 'GET':
        # 获取请求体中的数据
        page = int(request.GET.get('page'))
        users = User.objects.all().order_by('time')[(page - 1) * 10:page * 10]
        count = User.objects.all().count()
        print(count)
        data = []
        for user in users:
            data.append({'phone': user.phone, 'name': user.name, 'time': user.time, "statecode": user.stateCode})
        return JsonResponse({'code': 0, 'data': data, 'count': count})
    elif request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        User.objects.filter(name=name).update(stateCode="1")
        phone = User.objects.filter(name=name).first().phone
        Ban.objects.create(phone=phone, name=name, reason=data.get('reason'),
                           time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return JsonResponse({'code': 0, 'message': '用户已被封禁'})


@csrf_exempt
def banlist(request):
    if request.method == 'GET':
        page = int(request.GET.get('page'))
        bans = Ban.objects.all().order_by('time')[(page - 1) * 10:page * 10]
        count = Ban.objects.all().count()
        print("bancount:", count)
        data = []
        for ban in bans:
            data.append({'phone': ban.phone, 'name': ban.name, 'reason': ban.reason, 'time': ban.time})
        return JsonResponse({'code': 0, 'data': data, 'count': count})
    elif request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        print(name)
        User.objects.filter(name=name).update(stateCode="0")
        Ban.objects.filter(name=name).delete()
        return JsonResponse({'code': 0, 'message': '封禁已解除'})


@csrf_exempt
def search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        print(name)
        users = User.objects.filter(name=name)
        count = users.count()
        print("usercount:", count)
        data = []
        for user in users:
            data.append({'phone': user.phone, 'name': user.name, 'time': user.time, "statecode": user.stateCode})
        return JsonResponse({'code': 0, 'data': data, "count": count})


@csrf_exempt
def adminsearch(request):
    if request.method == 'POST':
        name = json.loads(request.body).get('name')
        users = Admin.objects.filter(name=name)
        count = users.count()
        print("admincount:", count)
        data = []
        for user in users:
            data.append({'phone': user.phone, 'name': user.name, 'time': user.time})
        return JsonResponse({'code': 0, 'data': data, "count": count})


@csrf_exempt
def grow(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        User.objects.filter(name=name).update(stateCode="2")
        phone = User.objects.filter(name=name).first().phone
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time)
        Admin.objects.create(phone=phone, name=name, time=time)
        return JsonResponse({'code': 0, 'message': '用户已设置为管理员'})


@csrf_exempt
def admin(request):
    if request.method == 'GET':
        page = int(request.GET.get('page'))
        users = Admin.objects.filter().all().order_by('time')[(page - 1) * 10:page * 10]
        count = Admin.objects.filter().all().count()
        print("admincount:", count)
        data = []
        for user in users:
            data.append({'phone': user.phone, 'name': user.name, 'time': user.time})
        return JsonResponse({'code': 0, 'data': data, 'count': count})
    elif request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        User.objects.filter(name=name).update(stateCode="0")
        print(name)
        Admin.objects.filter(name=name).delete()
        return JsonResponse({'code': 0, 'message': '管理员已被删除'})

# Create your views here.
