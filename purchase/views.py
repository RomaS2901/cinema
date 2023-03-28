from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from purchase.models import Order
from purchase.serializers import (
    OrderModelSerializer,
    CreateCartInputSerializer,
    CartOutputSerializer,
)
from purchase.services import (
    add_ticket_to_cart,
    buy_ticket,
    get_user_cart,
    remove_ticket_from_cart,
)


class OrderViewSet(GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @action(
        methods=["GET"],
        detail=False,
    )
    def cart(self, request):
        cart = get_user_cart(
            self.request.user,
            self.get_queryset(),
        )
        serializer = CartOutputSerializer(data=cart)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
        )

    @cart.mapping.post
    def add_to_cart(self, request):
        serializer = CreateCartInputSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        add_ticket_to_cart(
            ticket=serializer.validated_data["ticket"],
            buyer=self.request.user,
        )
        return Response(
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=["DELETE"],
        detail=True,
    )
    def delete_from_cart(
        self,
        request,
        pk: int,
    ):
        remove_ticket_from_cart(
            buyer=request.user,
            order_id=pk,
        )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        methods=["POST"],
        detail=True,
    )
    def buy_ticket(
        self,
        request,
        pk: int,
    ):
        buy_ticket(
            pk,
        )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
