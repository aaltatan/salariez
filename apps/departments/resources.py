from django.utils.translation import gettext as _

from import_export.resources import ModelResource, Field
from import_export.widgets import ForeignKeyWidget

from . import models


class DepartmentResource(ModelResource):
    
    name = Field('name', _('name').title())
    description = Field('description', _('description').title())
    department_id = Field('department_id', _('department id').title())
    level = Field('level', _('level').title())
    type = Field('type', _('type').title(), dehydrate_method='dehydrate_type')
    cost_center = Field('cost_center__name', _('cost center').title())
    parent = Field(
        'parent', 
        column_name=_('parent department').title(),
        widget=ForeignKeyWidget(models.Department, 'name')
    )
    
    def dehydrate_type(self, obj):
        return _('partial').title() if obj.is_leaf_node() else _('primary').title()

    class Meta:
        
        model = models.Department
        fields = [
            'department_id', 
            'name', 
            'type', 
            'level', 
            'parent',
            'cost_center', 
            'description', 
        ]
        export_order = [
            'tree_id', 'level', 'id'
        ]