from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from users.serializers import UserModelSerializer, LoginInputSerializer


class UserViewSet(
    CreateModelMixin,
    GenericViewSet,
):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = UserModelSerializer


@extend_schema(
    request=LoginInputSerializer,
)
@api_view(["POST"])
def login_api_view(
    request,
):
    serializer = LoginInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(
        request,
        # we use custom backend. email is used as username
        # for Django built-in authentication
        username=serializer.validated_data["email"],
        password=serializer.validated_data["password"],
    )

    if user is not None:
        login(request, user)
        return Response(
            status=status.HTTP_200_OK,
        )

    return Response(
        "Can't authenticate with provided credentials",
        status=status.HTTP_401_UNAUTHORIZED,
    )


@api_view(["POST"])
def logout_api_view(request):
    logout(request)
    return Response(
        status=status.HTTP_204_NO_CONTENT,
    )
