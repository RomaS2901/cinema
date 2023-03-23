from rest_framework.viewsets import ModelViewSet

from cinema_hall.serializers import (
    CinemaModelSerializer,
    HallModelSerializer,
    SeatModelSerializer,
)
from cinema_hall.models import Cinema, Hall, Seat


class CinemaViewSet(ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaModelSerializer


class HallViewSet(ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallModelSerializer


class SeatViewSet(ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatModelSerializer
