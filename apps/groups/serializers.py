from rest_framework import serializers

from . import models


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = (
            "id",
            "name",
            "slug",
        )
        read_only_fields = ("id", "slug")