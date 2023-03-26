import datetime
from typing import Any

import pytest
from rest_framework import status
from django.test.client import Client

from screening.models import ScreeningSession, Ticket


@pytest.mark.django_db
class TestScreeningSession:
    api_endpoint = "/api/screening_session/"
    response_date_format = "%Y-%m-%d"
    response_time_format = "%H:%M:%S"

    def test_create_screening_session(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data=screening_session_raw,
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_screening_session_failed_overlap_by_start_time(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
    ):
        ScreeningSession.objects.create(
            hall_id=screening_session_raw["hall"],
            movie_id=screening_session_raw["movie"],
            start_time=datetime.time(
                hour=1,
                minute=0,
                second=0,
            ),
            start_date=screening_session_raw["start_date"],
            end_date=screening_session_raw["end_date"],
        )
        response = api_test_client.post(
            self.api_endpoint,
            data={
                **screening_session_raw,
                "start_time": datetime.time(
                    hour=1,
                    minute=0,
                    second=0,
                ),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"start_time": ["Session time is already booked"]}

    def test_create_screening_session_failed_overlap_by_end_time(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
    ):
        ScreeningSession.objects.create(
            hall_id=screening_session_raw["hall"],
            movie_id=screening_session_raw["movie"],
            start_time=datetime.time(
                hour=1,
                minute=0,
                second=0,
            ),
            start_date=screening_session_raw["start_date"],
            end_date=screening_session_raw["end_date"],
        )
        response = api_test_client.post(
            self.api_endpoint,
            data={
                **screening_session_raw,
                "start_time": datetime.time(
                    hour=0,
                    minute=59,
                    second=59,
                ),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"start_time": ["Session time is already booked"]}

    def test_create_screening_session_failed_movie_rent_is_not_started(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
        movie_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data={
                **screening_session_raw,
                "start_date": movie_raw["rent_start_date"] - datetime.timedelta(days=1),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "start_date": [
                "Screening session start date can't be before movie rent start date. "
            ]
        }

    def test_create_screening_session_failed_movie_rent_is_over(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
        movie_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data={
                **screening_session_raw,
                "end_date": movie_raw["rent_end_date"] + datetime.timedelta(days=1),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "end_date": [
                "Screening session end date can't be after movie rent end date. "
            ]
        }

    def test_create_screening_session_failed_start_date_comes_after_end_date(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data={
                **screening_session_raw,
                "start_date": screening_session_raw["end_date"],
                "end_date": screening_session_raw["start_date"],
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"start_date": ["Start date comes after end date"]}

    def test_list_screening_session(
        self,
        api_test_client: Client,
        screening_session_with_tickets: ScreeningSession,
    ):
        response = api_test_client.get(
            self.api_endpoint,
        )

        assert response.json() == [
            {
                "end_date": screening_session_with_tickets.end_date.strftime(
                    self.response_date_format,
                ),
                "hall": screening_session_with_tickets.hall.id,
                "id": screening_session_with_tickets.id,
                "movie": screening_session_with_tickets.movie.id,
                "start_date": screening_session_with_tickets.start_date.strftime(
                    self.response_date_format,
                ),
                "start_time": screening_session_with_tickets.start_time.strftime(
                    self.response_time_format,
                ),
            }
        ]

    def test_screening_session_correct_calculates_end_date_property(
        self,
        screening_session_with_tickets: ScreeningSession,
        movie_raw: dict[str, Any],
        settings,
    ):
        assert (
            screening_session_with_tickets.end_time
            == (
                datetime.datetime.combine(
                    datetime.date.today(),
                    screening_session_with_tickets.start_time,
                )
                + datetime.timedelta(
                    seconds=screening_session_with_tickets.movie.duration
                    + settings.SCREENING_SESSION_BREAK,
                )
            ).time()
        )

    def test_create_screening_session_tickets_saved_correct(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
    ):
        api_test_client.post(
            self.api_endpoint,
            data=screening_session_raw,
        )

        response = api_test_client.get(
            self.api_endpoint,
        )
        ss_id = response.json()[0]["id"]
        screening_session = ScreeningSession.objects.get(id=ss_id)

        ss_running_days = (
            screening_session.end_date - screening_session.start_date
        ).days + 1  # inclusive end_date
        ss_seats = screening_session.hall.seats.count()

        # overall
        assert (
            Ticket.objects.filter(
                screening_id=ss_id,
                is_sold=False,
            ).count()
            == ss_running_days * ss_seats
        )
        # one session day
        assert (
            Ticket.objects.filter(
                screening_id=ss_id,
                session_date_time=datetime.datetime.combine(
                    screening_session.start_date,
                    screening_session.start_time,
                ),
                is_sold=False,
            ).count()
            == ss_seats
        )
