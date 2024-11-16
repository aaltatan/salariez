from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class ExchangeRateViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.ExchangeRate.objects.all()
    read_serializer_class = serializers.ExchangeRateReadSerializer
    write_serializer_class = serializers.ExchangeRateWriteSerializer
    filter_class = filters.ExchangeRateFilterSet