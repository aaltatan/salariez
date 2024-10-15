from django.utils.translation import gettext as _

from import_export import fields, resources

from . import models


class SpecializationRecourse(resources.ModelResource):
    
    name = fields.Field('name', column_name=_('name').title())
    is_academic = fields.Field(
        'is_academic', column_name=_('is academic').title()
    )
    description = fields.Field(
      'description', column_name=_('description').title()
    )

    class Meta:
        model = models.Specialization
        fields = ["name", "is_academic", "description"]
    
    def dehydrate_is_academic(self, obj):
        if obj.is_academic:
            return _('yes')
        return _('no')