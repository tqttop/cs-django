from datetime import datetime

from django.db import models


# Create your models here.
class User1(models.Model):
    id = models.AutoField(primary_key=True)
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


class Document(models.Model):
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='img/', default='default.jpg')
    videos = models.FileField(upload_to='videos/', default='default.mp4')


class Article(models.Model):
    Article_id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=13)
    time = models.DateTimeField(verbose_name='发表时间', default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    summary = models.CharField(verbose_name='文章简介', max_length=30, default='暂无简介')
    content = models.TextField(verbose_name='文章内容')
    readCount = models.IntegerField(verbose_name='阅读次数', default=0)
    goodCount = models.IntegerField(verbose_name='点赞次数', default=0)
    commentCount = models.IntegerField(verbose_name='评论数', default=0)
    author = models.ForeignKey(verbose_name='作者', to=User1, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(verbose_name='用户', to=User1, on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name='文章', to=Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')  # 用户对同一帖子只能点赞一次


class Comment(models.Model):
    time = models.DateTimeField(verbose_name='评论时间', default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    user = models.ForeignKey(verbose_name='评论', to=User1, on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name='文章', to=Article, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='评论内容')
