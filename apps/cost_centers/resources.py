from django.utils.translation import gettext as _

from import_export import fields, resources

from . import models


class CostCenterRecourse(resources.ModelResource):
    
    name = fields.Field('name', column_name=_('name').title())
    cost_center_accounting_id = fields.Field(
        'cost_center_accounting_id', 
        column_name=_('cost center id').title()
    )
    description = fields.Field(
        'description', column_name=_('description').title()
    )

    class Meta:
        model = models.CostCenter
        fields = ["name", "cost_center_accounting_id", "description"]
    
    # def dehydrate_name(self, obj):