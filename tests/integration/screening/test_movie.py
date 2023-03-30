from typing import Any

import pytest
from rest_framework import status
from django.test.client import Client

from screening.models import Movie


@pytest.mark.django_db
class TestMovie:
    api_endpoint = "/api/movie/"
    response_date_format = "%Y-%m-%d"

    def test_create_movie(
        self,
        api_test_client: Client,
        movie_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data=movie_raw,
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_list_movie(
        self,
        api_test_client: Client,
        movie: Movie,
    ):
        response = api_test_client.get(
            self.api_endpoint,
        )

        assert response.json() == [
            {
                "age_rating": movie.age_rating,
                "description": movie.description,
                "director": movie.director,
                "display_format": movie.display_format,
                "duration": movie.duration,
                "id": movie.id,
                "imdb_link": movie.imdb_link,
                "imdb_rating": movie.imdb_rating,
                "poster": None,
                "release_date": movie.release_date.strftime(
                    self.response_date_format,
                ),
                "rent_end_date": movie.rent_end_date.strftime(
                    self.response_date_format,
                ),
                "rent_start_date": movie.rent_start_date.strftime(
                    self.response_date_format,
                ),
                "title": movie.title,
            }
        ]
