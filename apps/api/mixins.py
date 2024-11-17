from django.utils.translation import gettext_lazy as _
from typing import Any
from django.db.models import Q
from pydantic import field_validator


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


class NameValidatorMixin:
    """
    Mixin for validating name.
    """

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value: str):
        if len(value) <= 3:
            raise ValueError(_("name must be at least 4 characters").title())

        if value in cls.Meta.model.objects.values_list("name", flat=True):
            raise ValueError(_("name already exists").title())

        return value
