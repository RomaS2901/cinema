from django.db import models


class Cinema(models.Model):
    name = models.CharField(
        max_length=128,
        db_index=True,
    )
    address = models.CharField(
        max_length=256,
    )

    class Meta:
        unique_together = (
            "name",
            "address",
        )


class Hall(models.Model):
    cinema = models.ForeignKey(
        Cinema,
        related_name="halls",
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=16,
        db_index=True,
    )

    class Meta:
        unique_together = (
            "name",
            "cinema",
        )

    def capacity(self):
        raise NotImplementedError


class Seat(models.Model):
    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name="seats",
    )
    number = models.PositiveIntegerField()
    row = models.PositiveIntegerField()

    class Meta:
        unique_together = (
            "number",
            "row",
            "hall",
        )
