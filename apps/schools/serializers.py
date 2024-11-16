from rest_framework import serializers

from apps.school_types.serializers import SchoolTypeSerializer

from . import models


class SchoolBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.School
        fields = (
            "id",
            "name",
            "school_type",
            "slug",
        )
        read_only_fields = ("id", "slug")


class SchoolReadSerializer(SchoolBaseSerializer):
    school_type = SchoolTypeSerializer(read_only=True)


class SchoolWriteSerializer(SchoolBaseSerializer):
    pass