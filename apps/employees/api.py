from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class EmployeeViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    read_serializer_class = serializers.EmployeeReadSerializer
    write_serializer_class = serializers.EmployeeWriteSerializer
    filter_class = filters.EmployeeFilterSet