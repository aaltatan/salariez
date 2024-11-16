from rest_framework import serializers

from . import models


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = (
            "id",
            "name",
            "order",
            "slug",
        )
        read_only_fields = ("id", "slug")