from rest_framework import serializers

from . import models


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobType
        fields = (
            "id",
            "name",
            "slug",
        )
        read_only_fields = ("id", "slug")
