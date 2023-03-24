from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser

from cinema_hall.serializers import (
    CinemaModelSerializer,
    HallModelSerializer,
)
from cinema_hall.models import Cinema, Hall


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


class HallViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Hall.objects.all()
    serializer_class = HallModelSerializer
    permission_classes = [
        IsAdminUser,
    ]
