from django.db import models


# Create your models here.
class User(models.Model):
    img = models.ImageField(upload_to='img/', default='default.jpg')
    stateCode = models.CharField(max_length=1, default='0')
    name = models.CharField(max_length=8)
    password = models.CharField(max_length=15)
    phone = models.CharField(max_length=11)
    time = models.CharField(max_length=50)
    role_choices = (
        ('user', '普通用户'),
        ('admin', '管理员'),
        ('root', '超级管理员')
    )
    role = models.CharField(max_length=16, choices=role_choices, default='user')


class Ban(models.Model):
    phone = models.CharField(max_length=11)
    name = models.CharField(max_length=8)
    reason = models.CharField(max_length=100)
    time = models.CharField(max_length=50)


class VerifyCode(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, verbose_name='手机号', unique=False)
    code = models.CharField(max_length=6)
