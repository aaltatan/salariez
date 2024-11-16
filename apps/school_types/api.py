from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class SchoolTypeViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.SchoolType.objects.all()
    serializer_class = serializers.SchoolTypeSerializer
    filter_class = filters.SchoolTypeFilterSet