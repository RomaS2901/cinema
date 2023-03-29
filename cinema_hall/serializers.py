from django.db.models import Count
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from cinema_hall.models import Cinema, Hall, Seat


class CinemaModelSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = Cinema
        fields = "__all__"


class SeatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = (
            "id",
            "row",
            "number",
        )


class HallModelSerializer(serializers.ModelSerializer):
    seats = SeatModelSerializer(
        many=True,
        read_only=True,
    )
    seats_tuple = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
    )

    class Meta:
        model = Hall
        fields = (
            "id",
            "name",
            "cinema",
            "seats",
            "seats_tuple",
        )

    def create(self, validated_data):
        hall = Hall.objects.create(
            cinema=validated_data["cinema"],
            name=validated_data["name"],
        )
        seats = []
        for row, seats_count in enumerate(
            validated_data["seats_tuple"],
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
