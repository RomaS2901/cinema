from django.db.models import Count
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from cinema_hall.models import Cinema, Hall, Seat


class CinemaModelSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = Cinema
        fields = "__all__"


class HallModelSerializer(serializers.ModelSerializer):
    seats_representation = serializers.SerializerMethodField()
    seats = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
    )

    class Meta:
        model = Hall
        fields = "__all__"

    @staticmethod
    def get_seats_representation(
        hall: Hall,
    ):
        return (
            hall.seats.values("row")
            .annotate(
                row_count=Count("row"),
            )
            .values_list(
                "row_count",
                flat=True,
            )
            .order_by("row")
        )

    def create(self, validated_data):
        hall = Hall.objects.create(
            cinema=validated_data["cinema"],
            name=validated_data["name"],
        )
        seats = []
        for row, seats_count in enumerate(
            validated_data["seats"],
            start=1,
        ):
            seats.extend(
                [
                    Seat(
                        hall=hall,
                        row=row,
                        number=number,
                    )
                    for number in range(
                        1,
                        seats_count + 1,
                    )
                ]
            )
        Seat.objects.bulk_create(seats)
        return hall
