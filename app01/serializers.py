from rest_framework import serializers

from app01 import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['phone', 'name', 'role', 'time', 'stateCode', ]


class BanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ban
        fields = ['phone', 'reason', 'time', 'name']

