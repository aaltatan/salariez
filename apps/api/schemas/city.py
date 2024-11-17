from ninja import ModelSchema, FilterSchema

from apps.cities.models import City

from .. import mixins


class CityFilterSchema(mixins.FiltersMixin, FilterSchema):
    name: str | None = None
    description: str | None = None


class CityCreateSchema(mixins.NameValidatorMixin, ModelSchema):
    name: str

    class Meta:
        model = City
        fields = ["name", "description"]


class CitySchema(ModelSchema):
    class Meta:
        model = City
        fields = ["id", "name", "slug", "description"]
