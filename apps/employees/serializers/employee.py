from rest_framework import serializers

from apps.nationalities.serializers import NationalitySerializer
from apps.areas.serializers import AreaReadSerializer
from apps.groups.serializers import GroupSerializer

from .. import models


class EmployeeBaseSerializer(serializers.ModelSerializer):
    short_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    job_age = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Employee
        fields = (
            "id",
            "fullname",
            "short_name",
            "firstname",
            "lastname",
            "father_name",
            "mother_name",
            "birth_place",
            "birth_date",
            "age",
            "gender",
            "national_id",
            "card_id",
            "civil_registry_office",
            "registry_office_name",
            "registry_office_id",
            "gender",
            "face_color",
            "eyes_color",
            "address",
            "special_signs",
            "card_date",
            "martial_status",
            "military_status",
            "religion",
            "current_address",
            "nationality",
            "area",
            "hire_date",
            "job_age",
            "notes",
            "groups",
            "slug",
        )
        read_only_fields = ("id", "slug", "short_name", "age", "job_age")


class EmployeeReadSerializer(EmployeeBaseSerializer):
    nationality = NationalitySerializer(read_only=True)
    area = AreaReadSerializer(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    gender = serializers.SerializerMethodField()
    martial_status = serializers.SerializerMethodField()
    military_status = serializers.SerializerMethodField()
    religion = serializers.SerializerMethodField()

    def get_religion(self, obj: models.Employee):
        return obj.get_religion_display()

    def get_military_status(self, obj: models.Employee):
        return obj.get_military_status_display()

    def get_martial_status(self, obj: models.Employee):
        return obj.get_martial_status_display()

    def get_gender(self, obj: models.Employee):
        return obj.get_gender_display()


class EmployeeWriteSerializer(EmployeeBaseSerializer):
    pass
