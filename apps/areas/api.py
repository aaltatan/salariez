from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class AreaViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Area.objects.all()
    filter_class = filters.AreaFilterSet
    read_serializer_class = serializers.AreaReadSerializer
    write_serializer_class = serializers.AreaWriteSerializer