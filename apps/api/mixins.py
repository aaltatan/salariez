from typing import Any

from django.db.models import Q


class FiltersMixin:
    """
    Mixin for filtering by name and description.
    """
    djangoql: str = ""

    def filter_name(self, value: str) -> Q:
        if not value:
            return Q()
        return Q(search__contains=value)

    def filter_description(self, value: str) -> Q:
        if not value:
            return Q()
        return Q(description__contains=value)

    def filter_djangoql(self, value: str) -> Q:
        return Q()

    def _filter_list(self, value: list[Any], field_name: str) -> Q:
        if not value:
            return Q()
        return Q(**{f"{field_name}__in": value})