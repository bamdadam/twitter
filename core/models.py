from django.db import models
from django.contrib.auth.models import User as DjangoUser


# Create your models here.


class SystemUser(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, null=True)
    at_name = models.CharField(max_length=255)
    # retweeted_tweets = models.ManyToManyField("Tweet", null=True)
    # pro_pic = models.ImageField(upload_to=get_image_upload_path, null=True)
    # relationship = models.ManyToManyField("SystemUser", through=RelationShip)
