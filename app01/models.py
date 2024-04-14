from django.db import models

# Create your models here.
class User(models.Model):
    stateCode = models.CharField(max_length=1, default='0')
    name = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    time = models.CharField(max_length=50)






class Admin(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    time = models.CharField(max_length=50)



class SuperAdmin(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)


class Ban(models.Model):
    phone = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    reason = models.CharField(max_length=100)
    time = models.CharField(max_length=50)


class VerifyCode(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, verbose_name='手机号', unique=False)
    code = models.CharField(max_length=6)