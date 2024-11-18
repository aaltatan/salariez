from django.utils.translation import gettext_lazy as _
from pydantic import field_validator


class NameValidatorMixin:
    """
    Mixin for validating name.
    """
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value: str):
        if len(value) <= 3:
            raise ValueError(_("name must be at least 4 characters").title())

        if len(value) > 255:
            raise ValueError(_("name must be at most 255 characters").title())

        if value in cls.Meta.model.objects.values_list("name", flat=True):
            raise ValueError(_("{} already exists").format(value).title())

        return value
