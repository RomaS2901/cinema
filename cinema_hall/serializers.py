from rest_framework import serializers

from cinema_hall.models import Cinema


class CinemaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = "__all__"
