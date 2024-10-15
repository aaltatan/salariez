from django.utils.translation import gettext as _

from import_export import fields, resources

from . import models


class SchoolRecourse(resources.ModelResource):
    
    name = fields.Field('name', column_name=_('name').title())
    school_type = fields.Field(
        'school_type__name', column_name=_('type').title()
    )
    nationality = fields.Field(
        'nationality__name', column_name=_('nationality').title()
    )
    description = fields.Field(
      'description', column_name=_('description').title()
    )

    class Meta:
        model = models.School
        fields = ["name", "school_type", "nationality", "description"]