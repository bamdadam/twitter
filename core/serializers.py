from rest_framework import serializers
from django.contrib.auth.models import User as DjangoUser
from rest_framework.exceptions import ValidationError

from core.models import SystemUser


class DjangoUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('password', 'email',)
        model = DjangoUser
        extra_kwargs = {
            'password': {'write_only': True}
        }

class CreateDjangoUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'password', 'email',)
        model = DjangoUser


    def save(self, **kwargs):
        user = DjangoUser(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user

class CreateSystemUserSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer()

    class Meta:
        model = SystemUser
        fields = ('user','at_name')

    def create(self, validated_data):
        # print('fcuk')
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


class UpdateSystemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        # fields = ('at_name', 'pro_pic')
        fields = ('at_name',)
