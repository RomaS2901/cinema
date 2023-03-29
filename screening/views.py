from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from screening.filters import ScreeningSessionFilter
from screening.models import Movie, ScreeningSession
from screening.serializers import MovieModelSerializer, ScreeningSessionModelSerializer


class MovieViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = MovieModelSerializer
    queryset = Movie.objects.all()
    permission_classes = [
        IsAdminUser,
    ]


class ScreeningSessionViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = ScreeningSessionModelSerializer
    queryset = ScreeningSession.objects.all()
    filterset_class = ScreeningSessionFilter

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
