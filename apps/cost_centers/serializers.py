from rest_framework import serializers

from . import models


class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CostCenter
        fields = (
            "id",
            "name",
            "cost_center_accounting_id",
            "slug",
        )
        read_only_fields = ("id", "slug")
