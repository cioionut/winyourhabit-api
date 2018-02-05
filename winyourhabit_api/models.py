from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    credit = models.FloatField(default=0.)
