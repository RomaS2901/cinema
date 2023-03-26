from django.contrib.auth import get_user_model
from django.db import models

from screening.models import Ticket


class Order(models.Model):
    class OrderOperation(models.TextChoices):
        PURCHASE = "PR", "Purchase"
        ADD_TO_CART = "CT", "Add to cart"
        RETURN = "RT", "Return"

    buyer = models.ForeignKey(
        get_user_model(),
        related_name="orders",
        on_delete=models.CASCADE,
    )
    ticket = models.ForeignKey(
        Ticket,
        related_name="orders",
        on_delete=models.CASCADE,
    )
    operation = models.CharField(
        max_length=2,
        choices=OrderOperation.choices,
    )
    date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "buyer",
            "ticket",
        )
