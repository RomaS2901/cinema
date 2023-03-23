from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model  # If used custom user model

from users.serializers import UserModelSerializer


class UserViewSet(
    CreateModelMixin,
    GenericViewSet,
):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = UserModelSerializer
