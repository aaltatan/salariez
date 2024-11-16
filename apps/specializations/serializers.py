from rest_framework import serializers

from . import models


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialization
        fields = (
            "id",
            "name",
            "is_specialist",
            "slug",
        )
        read_only_fields = ("id", "slug")