from django.utils.translation import gettext as _

from import_export import fields, resources

from . import models


class GroupRecourse(resources.ModelResource):
    
    name = fields.Field('name', column_name=_('name').title())
    description = fields.Field(
      'description', column_name=_('description').title()
    )

    class Meta:
        model = models.Group
        fields = ["name", "description"]
    
    # def dehydrate_name(self, obj):