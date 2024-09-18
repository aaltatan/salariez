from django.utils.translation import gettext as _

from import_export import fields, resources

from . import models


class AreaRecourse(resources.ModelResource):
    
    name = fields.Field('name', column_name=_('name').title())
    city = fields.Field(
      'city__name', column_name=_('city').title()
    )
    description = fields.Field(
      'description', column_name=_('description').title()
    )

    class Meta:
        model = models.City
        fields = ["name", "city", "description"]
    
    # def dehydrate_name(self, obj):