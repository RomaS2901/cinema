from django.db import models

from cinema_hall.models import Hall, Seat


class Movie(models.Model):
    class MovieDisplayFormat(models.TextChoices):
        THREE_DIMENSION = "3D", "3D"
        TWO_DIMENSION = "2D", "2D"

    title = models.CharField(
        max_length=200,
    )
    director = models.CharField(
        max_length=255,
    )
    display_format = models.CharField(
        max_length=2,
        default=MovieDisplayFormat.TWO_DIMENSION,
        choices=MovieDisplayFormat.choices,
    )
    release_date = models.DateField()
    description = models.TextField()
    poster = models.ImageField(
        upload_to="poster/",
        null=False,
    )
    age_rating = models.CharField(
        max_length=10,
        null=True,
    )
    imdb_rating = models.FloatField(
        null=True,
    )
    imdb_link = models.URLField(
        null=True,
    )
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()
    duration = models.PositiveIntegerField()

    class Meta:
        unique_together = (
            "title",
            "director",
            "rent_start_date",
            "rent_end_date",
        )


class ScreeningSession(models.Model):
    hall = models.ForeignKey(
        Hall,
        related_name="screening_sessions",
        on_delete=models.CASCADE,
    )
    movie = models.ForeignKey(
        Movie,
        related_name="screening_sessions",
        on_delete=models.CASCADE,
    )
    start_time = models.DateTimeField()


class Ticket(models.Model):
    screening = models.ForeignKey(
        ScreeningSession,
        related_name="tickets",
        on_delete=models.CASCADE,
    )
    seat = models.ForeignKey(
        Seat,
        related_name="seats",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    is_sold = models.BooleanField(
        default=False,
    )
