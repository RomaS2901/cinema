from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from cinema_hall.models import Cinema, Hall, Seat


class CinemaModelSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = Cinema
        fields = "__all__"


class HallModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = "__all__"


class SeatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"
