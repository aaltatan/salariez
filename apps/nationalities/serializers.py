from rest_framework import serializers

from . import models


class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nationality
        fields = (
            "id",
            "name",
            "is_local",
            "slug",
        )
        read_only_fields = ("id", "slug")
