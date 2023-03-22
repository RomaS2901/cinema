from rest_framework import serializers

from cinema_hall.models import Cinema, Hall, Seat


class CinemaModelSerializer(serializers.ModelSerializer):
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
