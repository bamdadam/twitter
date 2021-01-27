from django.db import models
from django.contrib.auth.models import User as DjangoUser


# Create your models here.


class SystemUser(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    at_name = models.CharField(max_length=255)
    retweeted_tweets = models.ManyToManyField("Tweet",)
    # pro_pic = models.ImageField(upload_to=get_image_upload_path, null=True)
    # relationship = models.ManyToManyField("SystemUser", through=RelationShip)


class Hashtag(models.Model):
    text = models.CharField(max_length=255)


class Tweet(models.Model):
    original_owner = models.ForeignKey(SystemUser, on_delete=models.CASCADE, related_name="owned_tweets")
    content = models.CharField(max_length=255)
    # image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag)
    like_count = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(SystemUser)
