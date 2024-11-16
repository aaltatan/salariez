from rest_framework import serializers

from apps.cost_centers.serializers import CostCenterSerializer

from . import models


class DepartmentBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Department
        fields = (
            "id",
            "name",
            "department_id",
            "cost_center",
            "parent",
            "slug",
        )
        read_only_fields = ("id", "slug")


class DepartmentReadSerializer(DepartmentBaseSerializer):
    cost_center = CostCenterSerializer(read_only=True)


class DepartmentWriteSerializer(DepartmentBaseSerializer):
    pass