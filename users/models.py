from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = "email"
    DEFAULT_BALANCE = 1000
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(
        unique=True,
    )
    balance = models.DecimalField(
        default=DEFAULT_BALANCE,
        max_digits=6,
        decimal_places=2,
    )
