from django.utils.translation import gettext as _

from import_export import fields, resources

from . import models


class SchoolTypeRecourse(resources.ModelResource):
    
    name = fields.Field('name', column_name=_('name').title())
    description = fields.Field(
      'description', column_name=_('description').title()
    )

    class Meta:
        model = models.SchoolType
        fields = ["name", "description"]