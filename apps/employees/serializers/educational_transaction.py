from rest_framework import serializers

from apps.educational_degrees.serializers import EducationalDegreeSerializer
from apps.specializations.serializers import SpecializationSerializer
from apps.schools.serializers import SchoolReadSerializer

from .. import models


class EducationalTransactionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EducationTransaction
        fields = (
            "id",
            "employee",
            "degree",
            "specialization",
            "school",
            "start_date",
            "end_date",
            "is_current",
            "is_academic",
            "order",
            "slug",
        )
        read_only_fields = ("id", "slug")


class EducationalTransactionReadSerializer(
    EducationalTransactionBaseSerializer
):
    degree = EducationalDegreeSerializer(read_only=True)
    specialization = SpecializationSerializer(read_only=True)
    school = SchoolReadSerializer(read_only=True)


class EducationalTransactionWriteSerializer(
    EducationalTransactionBaseSerializer
):
    pass
