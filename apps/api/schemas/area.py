from django.db.models import Q
from ninja import ModelSchema, FilterSchema

from apps.areas.models import Area

from .utils import FiltersMixin
from .city import CitySchema


class AreaFilterSchema(FiltersMixin, FilterSchema):
    name: str | None = None
    description: str | None = None
    cities: list[str] = []

    def filter_cities(self, value: list[str]) -> Q:
        return self._filter_list(value, "city__name")


class AreaCreateSchema(ModelSchema):
    class Meta:
        model = Area
        fields = ["name", "description"]


class AreaInSchema(ModelSchema):
    class Meta:
        model = Area
        fields = ["name", "city", "description"]


class AreaSchema(ModelSchema):
    city: CitySchema

    class Meta:
        model = Area
        fields = ["id", "name", "city", "slug", "description"]
