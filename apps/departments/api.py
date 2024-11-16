from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class DepartmentViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    read_serializer_class = serializers.DepartmentReadSerializer
    write_serializer_class = serializers.DepartmentWriteSerializer
    filter_class = filters.DepartmentFilterSet