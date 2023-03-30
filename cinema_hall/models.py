from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Cinema(models.Model):
    name = models.CharField(
        max_length=128,
    )
    address = models.CharField(
        max_length=256,
    )
    phone_number = PhoneNumberField(
        null=True,
        blank=True,
    )
    facebook_social_link = models.URLField(
        null=True,
        blank=True,
    )
    instagram_social_link = models.URLField(
        null=True,
        blank=True,
    )
    youtube_social_link = models.URLField(
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = (
            "name",
            "address",
        )

    def __str__(self):
        return self.name


class Hall(models.Model):
    cinema = models.ForeignKey(
        Cinema,
        related_name="halls",
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=16,
    )

    class Meta:
        unique_together = (
            "name",
            "cinema",
        )

    def __str__(self):
        return self.name


class Seat(models.Model):
    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name="seats",
    )
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = (
            "hall",
            "row",
            "number",
        )

    def __str__(self):
        return f"<{self.row} - {self.number}>"
