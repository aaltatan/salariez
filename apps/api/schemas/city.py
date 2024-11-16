from ninja import ModelSchema, FilterSchema

from apps.cities.models import City

from .utils import FiltersMixin


class CityFilterSchema(FiltersMixin, FilterSchema):
    name: str | None = None
    description: str | None = None


class CityCreateSchema(ModelSchema):
    class Meta:
        model = City
        fields = ["name", "description"]


class CitySchema(ModelSchema):
    class Meta:
        model = City
        fields = ["id", "name", "slug", "description"]
