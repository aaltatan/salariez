from ninja import FilterSchema, ModelSchema

from apps.cities.models import City

from .. import mixins
from ..validators.name import NameValidatorMixin


class CityFilterSchema(mixins.FiltersMixin, FilterSchema):
    name: str | None = None
    description: str | None = None


class CityCreateSchema(NameValidatorMixin, ModelSchema):
    class Meta:
        model = City
        fields = "name", "description"


class CityUpdateSchema(NameValidatorMixin, ModelSchema):
    class Meta:
        model = City
        exclude = "id", "search"


class CitySchema(ModelSchema):
    class Meta:
        model = City
        exclude = "search",
