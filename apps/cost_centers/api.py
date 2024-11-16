from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class CostCenterViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.CostCenter.objects.all()
    serializer_class = serializers.CostCenterSerializer
    filter_class = filters.CostCenterFilterSet
