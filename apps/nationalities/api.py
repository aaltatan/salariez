from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class NationalityViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Nationality.objects.all()
    serializer_class = serializers.NationalitySerializer
    filter_class = filters.NationalityFilterSet