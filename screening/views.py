from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAdminUser

from screening.models import Movie
from screening.serializers import MovieModelSerializer


class MovieViewSet(
    CreateModelMixin,
    GenericViewSet,
):
    serializer_class = MovieModelSerializer
    queryset = Movie.objects.all()
    permission_classes = [
        IsAdminUser,
    ]
