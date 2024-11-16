from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class StatusViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    filter_class = filters.StatusFilterSet