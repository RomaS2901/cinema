from rest_framework import serializers

from purchase.models import Order
from screening.models import Ticket


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
    )


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
