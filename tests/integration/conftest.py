import datetime

from pytest import fixture
from django.contrib.auth import get_user_model
from django.test.client import Client

from cinema_hall.models import Cinema, Hall, Seat
from screening.models import Movie, ScreeningSession, Ticket

user_model = get_user_model()


@fixture
def test_superuser():
    return get_user_model().objects.create(
        username="test",
        email="test@exmaple.com",
        password="test",
        is_superuser=True,
        is_active=True,
        is_staff=True,
    )


@fixture
def api_test_client(
    test_superuser,
):
    client = Client()
    client.force_login(test_superuser)
    return client


@fixture
def cinema_raw():
    return {
        "phone_number": "+380981111111",
        "name": "Cinema",
        "address": "Cinema st.",
        "facebook_social_link": "https://www.facebook.com/my-cinema/",
        "instagram_social_link": "https://www.instagram.com/my-cinema/",
        "youtube_social_link": "https://www.youtube.com/my-cinema/",
    }


@fixture
def cinema(
    cinema_raw,
):
    return Cinema.objects.create(
        **cinema_raw,
    )


@fixture
def hall_raw(
    cinema,
):
    return {
        "cinema": cinema.id,
        "seats": [
            1,
            2,
            3,
            4,
            5,
        ],
        "name": "First Hall",
    }


@fixture
def hall_with_seats(
    hall_raw,
):
    hall = Hall.objects.create(
        name=hall_raw["name"],
        cinema_id=hall_raw["cinema"],
    )
    seats = []
    for row, seats_count in enumerate(
        hall_raw["seats"],
        start=1,
    ):
        seats.extend(
            [
                Seat(
                    hall=hall,
                    row=row,
                    number=number,
                )
                for number in range(
                    1,
                    seats_count + 1,
                )
            ]
        )
    Seat.objects.bulk_create(seats)
    return hall


@fixture
def movie_raw():
    return {
        "title": "Movie Title",
        "director": "Test Director",
        "display_format": "2D",
        "release_date": datetime.date(
            year=2000,
            month=1,
            day=1,
        ),
        "description": "Movie description",
        "rent_start_date": datetime.date.today(),
        "rent_end_date": datetime.date.today() + datetime.timedelta(days=14),
        "duration": 60 * 120,
    }


@fixture
def movie(movie_raw):
    return Movie.objects.create(**movie_raw)


@fixture
def screening_session_raw(
    hall_with_seats,
    movie,
):
    return {
        "hall": hall_with_seats.id,
        "movie": movie.id,
        "price": 100,
        "start_time": datetime.time(
            hour=0,
            minute=0,
            second=0,
        ),
        "start_date": datetime.date.today(),
        "end_date": datetime.date.today()
        + datetime.timedelta(
            days=7,
        ),
    }


@fixture
def screening_session_with_tickets(
    screening_session_raw,
):
    screening_session = ScreeningSession.objects.create(
        hall_id=screening_session_raw["hall"],
        movie_id=screening_session_raw["movie"],
        start_time=screening_session_raw["start_time"],
        start_date=screening_session_raw["start_date"],
        end_date=screening_session_raw["end_date"],
    )
    # create ticket for each seat in the hall with given price
    hall_seat_ids = screening_session.hall.seats.values_list(
        "id",
        flat=True,
    )
    tickets = []
    delta = screening_session.end_date - screening_session.start_date
    for seat_id in hall_seat_ids:
        for session_day in range(delta.days + 1):
            tickets.append(
                Ticket(
                    screening=screening_session,
                    seat_id=seat_id,
                    price=screening_session_raw["price"],
                    session_date_time=datetime.datetime.combine(
                        screening_session.start_date
                        + datetime.timedelta(
                            days=session_day,
                        ),
                        screening_session.start_time,
                    ),
                )
            )

    Ticket.objects.bulk_create(
        tickets,
    )
    return screening_session
