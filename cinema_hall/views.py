from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser

from cinema_hall.serializers import (
    CinemaModelSerializer,
    HallModelSerializer,
    SeatModelSerializer,
)
from cinema_hall.models import Cinema, Hall, Seat


class CinemaViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Cinema.objects.all()
    serializer_class = CinemaModelSerializer
    permission_classes = [
        IsAdminUser,
    ]


class HallViewSet(ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallModelSerializer


class SeatViewSet(ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatModelSerializer
