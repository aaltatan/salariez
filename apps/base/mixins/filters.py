from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class FiltersMixins:

    def filter_name(self, queryset, name, value):
        keywords = value.split(" ")
        stmt = Q()
        for keyword in keywords:
            stmt &= Q(search__contains=keyword)
        return queryset.filter(stmt)
