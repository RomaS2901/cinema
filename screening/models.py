from django.db import models

from cinema_hall.models import Hall, Seat


class Movie(models.Model):
    title = models.CharField(
        max_length=200,
    )
    release_date = models.DateField()
    director = models.CharField(
        max_length=200,
    )
    description = models.TextField()
    imdb_ukr = models.URLField()
    duration = models.PositiveIntegerField()
    start_date_right_to_rent = models.DateField()
    end_date_right_to_rent = models.DateField()

    class Meta:
        unique_together = (
            "title",
            "director",
            "start_date_right_to_rent",
            "end_date_right_to_rent",
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
