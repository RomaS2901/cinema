import pytest
from rest_framework import status
from django.test.client import Client

from cinema_hall.models import Cinema


@pytest.mark.django_db
class TestCinema:
    api_endpoint = "/api/cinema/"

    def test_create_cinema(
        self,
        api_test_client: Client,
        cinema_raw: dict[str, str],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data=cinema_raw,
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_list_cinema(
        self,
        api_test_client: Client,
        cinema: Cinema,
    ):
        response = api_test_client.get(
            self.api_endpoint,
        )

        assert response.json() == [
            {
                "id": cinema.id,
                "name": cinema.name,
                "address": cinema.address,
                "phone_number": cinema.phone_number,
                "facebook_social_link": cinema.facebook_social_link,
                "instagram_social_link": cinema.instagram_social_link,
                "youtube_social_link": cinema.youtube_social_link,
            }
        ]
