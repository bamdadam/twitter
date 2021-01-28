from rest_framework import serializers
from django.contrib.auth.models import User as DjangoUser
from rest_framework.exceptions import ValidationError

from core.models import SystemUser, Tweet, Hashtag, RelationShip, Event


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
        fields = ('user', 'at_name')

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


class SystemUserSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer()

    class Meta:
        model = SystemUser
        fields = ('id', 'user', 'at_name')


class CreateTweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('content',)

        # fields = ('content', 'image',)

    def create(self, validated_data):
        tweet = Tweet.objects.create(**validated_data)
        content = validated_data['content']
        words = content.split(" ")
        hashtags = []
        for word in words:
            if word.startswith('#'):
                hashtag, is_created = Hashtag.objects.get_or_create(text=word)
                hashtags.append(hashtag)
            for hashtag in hashtags:
                tweet.hashtags.add(hashtag)
                tweet.save()
        return tweet
        #     try:
        #         hashtag = Hashtag.objects.get(text = word)
        #         hashtags.append(hashtag)
        #     except Hashtag.DoesNotExist:
        #         hashtag = Hashtag.objects.create(text=word)
        #         hashtags.append(hashtag)
        # for hashtag in hashtags:
        #     tweet.hashtags.add(hashtag)


class RelationShipSerializer(serializers.ModelSerializer):
    second_user = SystemUserSerializer(read_only=True)
    first_user = SystemUserSerializer(read_only=True)
    relationship_type = serializers.CharField(default='F')
    second_user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RelationShip
        fields = ('first_user', 'second_user_id', 'relationship_type', 'second_user', 'id')

    def create(self, validated_data):
        validated_data['second_user'] = SystemUser.objects.get(id=validated_data['second_user_id'])
        if validated_data['second_user'] == validated_data['first_user']:
            raise ValidationError({'details': 'can not follow myself'})
        return self.Meta.model.objects.create(**validated_data)


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('original_owner', 'content', 'hashtags', 'like_count', 'id')

# class UserAndTweetserializer(serializers.ModelSerializer):
#     class Meta:
#         model = SystemUser
#         fields = ('owned_tweets',)
#
#     def create(self, validated_data):
#         pass
