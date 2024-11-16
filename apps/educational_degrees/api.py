from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class EducationalDegreeViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.EducationalDegree.objects.all()
    serializer_class = serializers.EducationalDegreeSerializer
    filter_class = filters.EducationalDegreeFilterSet