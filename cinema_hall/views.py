from rest_framework.viewsets import ModelViewSet

from cinema_hall.serializers import CinemaModelSerializer
from cinema_hall.models import Cinema


class CinemaModelViewSet(ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaModelSerializer
