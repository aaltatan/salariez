from django.utils.translation import gettext as _

from import_export import fields, resources

from . import models


class CurrencyRecourse(resources.ModelResource):
    
    name = fields.Field('name', column_name=_('name').title())
    description = fields.Field(
      'description', column_name=_('description').title()
    )
    is_local = fields.Field('is_local', column_name=_('local').title())

    class Meta:
        model = models.Currency
        fields = ["name", "is_local", "description"]
    
    def dehydrate_is_local(self, obj):
        return _('local').title() if obj.is_local else _('foreign').title()
