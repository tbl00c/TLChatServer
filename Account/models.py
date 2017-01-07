#coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phoneNumber = models.CharField(max_length=11)
    avatar = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "user"


class UserPermission(models.Model):
    user = models.ForeignKey(User, related_name="permission")