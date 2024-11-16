from rest_framework import serializers

from . import models


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = (
            "id",
            "name",
            "has_salary",
            "slug",
        )
        read_only_fields = ("id", "slug")