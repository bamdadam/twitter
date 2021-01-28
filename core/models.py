from django.db import models
from django.contrib.auth.models import User as DjangoUser


# Create your models here.


class RelationShip(models.Model):
    following = 'F'
    blocked = 'B'
    relationship_choices = ((following, 'following'), (blocked, 'blocked'))
    first_user = models.ForeignKey("SystemUser", on_delete=models.CASCADE, related_name="first_user_relationship")
    second_user = models.ForeignKey("SystemUser", on_delete=models.CASCADE, related_name="second_user_relationship")
    relationship_type = models.CharField(max_length=1, choices=relationship_choices)


class SystemUser(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='systemuser')
    at_name = models.CharField(max_length=255)
    retweeted_tweets = models.ManyToManyField("Tweet", )
    # pro_pic = models.ImageField(upload_to=get_image_upload_path, null=True)
    relationship = models.ManyToManyField("SystemUser", through=RelationShip)


class Hashtag(models.Model):
    text = models.CharField(max_length=255)


class Tweet(models.Model):
    original_owner = models.ForeignKey(
        SystemUser, on_delete=models.CASCADE, related_name="owned_tweets")
    content = models.CharField(max_length=255)
    # image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag)
    like_count = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(SystemUser)


class Event(models.Model):
    followed = 'F'
    liked_tweet = 'L'
    retweeted = 'R'
    event_type_choices = ((followed, 'followed'), (liked_tweet, 'liked_tweet'), (retweeted, 'retweeted'))
    owner = models.ForeignKey(SystemUser, on_delete=models.CASCADE, related_name='event_owner')
    second_user = models.ForeignKey(SystemUser, on_delete=models.CASCADE, related_name='event_second_user')
    event_type = models.CharField(max_length=1, choices=event_type_choices)
