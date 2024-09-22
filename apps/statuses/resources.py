from django.utils.translation import gettext as _

from import_export import fields, resources

from . import models


class StatusRecourse(resources.ModelResource):
    
    name = fields.Field('name', column_name=_('name').title())
    description = fields.Field(
      'description', column_name=_('description').title()
    )
    has_salary = fields.Field(
        'has_salary', column_name=_('has salary').title()
    )

    class Meta:
        model = models.Status
        fields = ["name", "has_salary", "description"]
    
    def dehydrate_has_salary(self, obj):
        return _('has salary').title() if obj.has_salary else _('has not salary').title()
