from pytest import fixture
from django.contrib.auth import get_user_model
from django.test.client import Client

from cinema_hall.models import Cinema, Hall, Seat

user_model = get_user_model()


@fixture
def test_superuser():
    from users.models import User

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
