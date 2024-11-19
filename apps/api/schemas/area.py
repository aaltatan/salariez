from django.db.models import Q
from ninja import ModelSchema, FilterSchema, Schema

from apps.areas.models import Area

from ..mixins import FiltersMixin
from ..validators.name import NameValidatorMixin
from .city import CitySchema


class AreaFilterSchema(FiltersMixin, FilterSchema):
    name: str | None = None
    description: str | None = None
    cities: list[str] = []

    def filter_cities(self, value: list[str]) -> Q:
        return self._filter_list(value, "city__name")


class AreaCreateSchema(NameValidatorMixin, Schema):

    name: str
    city_id: int
    description: str = ""
    


class AreaSchema(ModelSchema):
    city: CitySchema

    class Meta:
        model = Area
        exclude = ("search",)
