from rest_framework import viewsets

from apps.base.mixins import ViewSetMixin

from . import filters, models, serializers


class GroupViewSet(ViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    filter_class = filters.GroupFilterSet