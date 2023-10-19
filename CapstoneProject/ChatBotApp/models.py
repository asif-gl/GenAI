from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    technologies = models.CharField(max_length=512, blank=True)
    goals = models.CharField(max_length=512, blank=True)