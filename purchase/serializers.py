from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from purchase.models import Order
from cinema_hall.models import Seat
from screening.models import Ticket, ScreeningSession


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = (
            "operation",
            "date",
            "buyer",
        )


class TicketModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


# noinspection PyAbstractClass
class CreateCartInputSerializer(
    serializers.Serializer,
):
    ticket = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(),
        required=False,
        allow_null=True,
    )
    session = serializers.PrimaryKeyRelatedField(
        queryset=ScreeningSession.objects.all(), required=False, allow_null=True
    )
    seat = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(),
        required=False,
        allow_null=True,
    )
    session_date_time = serializers.DateTimeField(
        required=False,
        allow_null=True,
    )

    def validate(self, attrs):
        if not attrs.get("ticket") and not all(
            [
                attrs.get("session"),
                attrs.get("seat"),
                attrs.get("session_date_time"),
            ],
        ):
            raise ValidationError(
                "Both session, seat, session_date_time attrs required if no ticket provided",
            )

        return attrs


# noinspection PyAbstractClass
class CartItemTicketOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    is_sold = serializers.BooleanField()
    session_date_time = serializers.DateTimeField()


# noinspection PyAbstractClass
class CartItemOutputSerializer(
    serializers.Serializer,
):
    id = serializers.IntegerField()
    ticket = CartItemTicketOutputSerializer()


# noinspection PyAbstractClass
class CartOutputSerializer(
    serializers.Serializer,
):
    items = CartItemOutputSerializer(
        many=True,
    )
    total_price = serializers.FloatField()
