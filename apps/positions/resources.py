from django.utils.translation import gettext as _

from import_export import fields, resources

from . import models


class PositionRecourse(resources.ModelResource):
    
    name = fields.Field('name', column_name=_('name').title())
    order = fields.Field('order', column_name=_('order').title())
    description = fields.Field(
      'description', column_name=_('description').title()
    )

    class Meta:
        model = models.Position
        fields = ["name", "order", "description"]
    
    # def dehydrate_name(self, obj):