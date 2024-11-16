from rest_framework import serializers

from . import models


class SchoolTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolType
        fields = (
            "id",
            "name",
            "slug",
        )
        read_only_fields = ("id", "slug")