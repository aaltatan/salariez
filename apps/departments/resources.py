from django.utils.translation import gettext as _

from import_export.resources import ModelResource, Field
from import_export.widgets import ForeignKeyWidget

from . import models


class DepartmentResource(ModelResource):
    
    name = Field('name', _('name').title())
    description = Field('description', _('description').title())
    parent = Field(
        'parent', 
        column_name=_('parent department').title(),
        widget=ForeignKeyWidget(
            models.Department,
            'name'
        )
    )
    
    class Meta:
        
        model = models.Department
        fields = [
            'name', 'description', 'parent'
        ]