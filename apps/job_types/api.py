from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class JobTypeViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.JobType.objects.all()
    serializer_class = serializers.JobTypeSerializer
    filter_class = filters.JobTypeFilterSet