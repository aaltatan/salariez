from rest_framework import serializers

from .models import EducationalDegree


class EducationalDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalDegree
        fields = (
            "id",
            "name",
            "is_academic",
            "order",
            "slug",
        )
        read_only_fields = ("id", "slug")
