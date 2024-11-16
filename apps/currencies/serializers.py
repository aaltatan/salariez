from rest_framework import serializers

from . import models


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = (
            "id",
            "name",
            "short_name",
            "fraction_name",
            "is_local",
            "slug",
        )
        read_only_fields = ("id", "slug")