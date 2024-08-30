from django.utils.translation import gettext as _

from import_export import fields, resources

from . import models


class FacultyRecourse(resources.ModelResource):
    
    name = fields.Field('name', column_name=_('name').title())

    class Meta:
        model = models.Faculty
        fields = ["name"]
    
    # def dehydrate_name(self, obj):