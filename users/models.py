from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    DEFAULT_BALANCE = 1000

    email = models.EmailField(
        unique=True,
    )
    balance = models.FloatField(
        default=DEFAULT_BALANCE,
    )
