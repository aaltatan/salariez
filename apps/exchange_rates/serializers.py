from rest_framework import serializers

from apps.currencies.serializers import CurrencySerializer

from . import models


class ExchangeRateBaseSerializer(serializers.ModelSerializer):
    
    input_rate = serializers.DecimalField(
        max_digits=20,
        decimal_places=8,
        write_only=True,
    )
    is_inverse = serializers.BooleanField(write_only=True)

    class Meta:
        model = models.ExchangeRate
        fields = (
            "id",
            "date",
            "rate",
            "input_rate",
            "is_inverse",
            "currency",
            "slug",
        )
        read_only_fields = ("id", "slug")


class ExchangeRateReadSerializer(ExchangeRateBaseSerializer):
    currency = CurrencySerializer(read_only=True)


class ExchangeRateWriteSerializer(ExchangeRateBaseSerializer):
    pass