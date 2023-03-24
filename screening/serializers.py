from rest_framework import serializers

from screening.models import Movie


class MovieModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"
