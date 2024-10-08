# Generated by Django 5.0.4 on 2024-05-21 04:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('Article_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=13, verbose_name='文章标题')),
                ('time', models.DateTimeField(default='2024-05-21 12:06:42', verbose_name='发表时间')),
                ('summary', models.CharField(default='暂无简介', max_length=30, verbose_name='文章简介')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('readCount', models.IntegerField(default=0, verbose_name='阅读次数')),
                ('goodCount', models.IntegerField(default=0, verbose_name='点赞次数')),
                ('commentCount', models.IntegerField(default=0, verbose_name='评论数')),
            ],
        ),
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11)),
                ('name', models.CharField(max_length=8)),
                ('reason', models.CharField(max_length=100)),
                ('time', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('img', models.ImageField(default='default.jpg', upload_to='img/')),
                ('videos', models.FileField(default='default.mp4', upload_to='videos/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(default='default.jpg', upload_to='img/')),
                ('stateCode', models.CharField(default='0', max_length=1)),
                ('name', models.CharField(max_length=8)),
                ('password', models.CharField(max_length=15)),
                ('phone', models.CharField(max_length=11)),
                ('time', models.CharField(max_length=50)),
                ('role', models.CharField(choices=[('user', '普通用户'), ('admin', '管理员'), ('root', '超级管理员')], default='user', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default='2024-05-21 12:06:42', verbose_name='评论时间')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.article', verbose_name='文章')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user', verbose_name='评论')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user', verbose_name='作者'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.article', verbose_name='文章')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user', verbose_name='用户')),
            ],
            options={
                'unique_together': {('user', 'article')},
            },
        ),
    ]
