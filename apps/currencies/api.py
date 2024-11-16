from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class CurrencyViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer
    filter_class = filters.CurrencyFilterSet