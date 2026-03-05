from django.db import models

from django.contrib.auth.models import User, AbstractUser

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)


#
# class User(models.Model):
#     first_name = models.CharField(max_length=100, null=False, blank=False)
#     last_name = models.CharField(max_length=100, null=False, blank=False)
#
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=11, null=False, blank=False)
#     password = models.CharField(max_length=100, null=False, blank=False)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)