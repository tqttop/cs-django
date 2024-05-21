from rest_framework import serializers

from app01 import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User1
        fields = ['phone', 'name', 'role', 'time', 'stateCode','password']


class BanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ban
        fields = ['phone', 'reason', 'time', 'name']


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = ['title', 'img', 'videos']


class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ['title', 'content', 'time', 'author', 'Article_id', 'readCount', 'goodCount', 'commentCount',
                  'summary', 'Article_id']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['content', 'time', 'user', 'article']