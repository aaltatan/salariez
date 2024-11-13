from rest_framework import serializers
from . import models
from apps.cities.serializers import CitySerializer


class AreaBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Area
        fields = (
            "id",
            "name",
            "city",
            "description",
            "slug",
        )
        read_only_fields = ("id", "slug")


class AreaReadSerializer(AreaBaseSerializer):
    city = CitySerializer(read_only=True)


class AreaWriteSerializer(AreaBaseSerializer):
    pass
