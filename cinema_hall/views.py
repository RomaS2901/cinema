from rest_framework.viewsets import ModelViewSet

from cinema_hall.serializers import (
    CinemaModelSerializer,
    HallModelSerializer,
    SeatModelSerializer,
)
from cinema_hall.models import Cinema, Hall, Seat


class CinemaModelViewSet(ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaModelSerializer


class HallModelViewSet(ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallModelSerializer


class SeatModelViewSet(ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatModelSerializer
