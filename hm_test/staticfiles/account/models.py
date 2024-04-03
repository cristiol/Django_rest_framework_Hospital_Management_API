import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(max_length=150)
    status=models.BooleanField(default=False)

