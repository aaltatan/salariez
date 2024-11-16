from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class JobSubtypeViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.JobSubtype.objects.all()
    read_serializer_class = serializers.JobSubtypeReadSerializer
    write_serializer_class = serializers.JobSubtypeWriteSerializer
    filter_class = filters.JobSubtypeFilterSet
