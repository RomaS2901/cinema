from django_filters import rest_framework, OrderingFilter

from screening.models import ScreeningSession


class ScreeningSessionFilter(rest_framework.FilterSet):
    o = OrderingFilter(
        fields=(
            (
                "start_time",
                "start_time",
            ),
            (
                "start_date",
                "start_date",
            ),
            (
                "end_date",
                "end_date",
            ),
            (
                "tickets__price",
                "price",
            ),
        )
    )

    class Meta:
        model = ScreeningSession
        fields = {
            "start_time": [
                "gte",
            ],
            "start_date": [
                "exact",
            ],
            "end_date": [
                "exact",
            ],
            "hall": [
                "exact",
            ],
        }
