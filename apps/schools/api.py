from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class SchoolViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.School.objects.all()
    read_serializer_class = serializers.SchoolReadSerializer
    write_serializer_class = serializers.SchoolWriteSerializer
    filter_class = filters.SchoolFilterSet