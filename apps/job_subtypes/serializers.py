from rest_framework import serializers

from apps.job_types.serializers import JobTypeSerializer

from . import models


class JobSubtypeBaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.JobSubtype
        fields = (
            "id",
            "name",
            "job_type",
            "slug",
        )
        read_only_fields = ("id", "slug")


class JobSubtypeReadSerializer(JobSubtypeBaseSerializer):
    job_type = JobTypeSerializer(read_only=True)


class JobSubtypeWriteSerializer(JobSubtypeBaseSerializer):
    pass