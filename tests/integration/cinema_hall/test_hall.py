from typing import Any

import pytest
from rest_framework import status
from django.test.client import Client

from cinema_hall.models import Hall


@pytest.mark.django_db
class TestHall:
    api_endpoint = "/api/hall/"

    def test_create_hall(
        self,
        api_test_client: Client,
        hall_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data=hall_raw,
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_list_hall(
        self,
        api_test_client: Client,
        hall_with_seats: Hall,
        hall_raw: dict[str, Any],
    ):
        response = api_test_client.get(
            self.api_endpoint,
        )

        assert response.json() == [
            {
                "id": hall_with_seats.id,
                "cinema": hall_with_seats.cinema_id,
                "name": hall_with_seats.name,
                "seats_representation": hall_raw["seats"],
            },
        ]
