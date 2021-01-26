from rest_framework import serializers
from django.contrib.auth.models import User as DjangoUser
from rest_framework.exceptions import ValidationError

from core.models import SystemUser


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('password', 'email',)
        model = DjangoUser


class CreateDjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'password', 'email',)
        model = DjangoUser


class CreateSystemUserSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer()

    class Meta:
        fields = '__all__'
        model = SystemUser

    def create(self, validated_data):
        django_user_data = validated_data.pop('user')
        django_user_data.update({
            "username": django_user_data["email"]
        })
        django_user_serializer = CreateDjangoUserSerializer(data=django_user_data)
        django_user_serializer.is_valid(raise_exception=True)
        django_user = django_user_serializer.save()
        validated_data.update({
            "user": django_user
        })
        try:
            system_user = SystemUser.objects.create(**validated_data)
            return system_user
        except Exception:
            django_user.delete()
            raise ValidationError("system user data is invalid")
