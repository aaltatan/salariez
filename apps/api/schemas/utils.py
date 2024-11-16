from typing import Any
from django.db.models import Q
from ninja import Schema


class FiltersMixin:
    """
    Mixin for filtering by name and description.
    """

    def filter_name(self, value: str) -> Q:
        if not value:
            return Q()
        return Q(search__contains=value)

    def filter_description(self, value: str) -> Q:
        if not value:
            return Q()
        return Q(description__contains=value)

    def _filter_list(self, value: list[Any], field_name: str) -> Q:
        if not value:
            return Q()
        return Q(**{f"{field_name}__in": value})


class PaginationSchema(Schema):
    offset: int = 0
    limit: int = 10


class OrderBySchema[T](Schema):
    fields: list[T] = []


class ListWrapperSchema[T](Schema):
    status: int
    total: int
    offset: int
    limit: int
    results: T
