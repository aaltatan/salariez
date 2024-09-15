from django.utils.translation import gettext as _

from import_export import fields, resources

from . import models


class JobSubtypeRecourse(resources.ModelResource):
    
    name = fields.Field('name', column_name=_('name').title())
    job_type = fields.Field(
      'job_type__name', column_name=_('job type').title()
    )
    description = fields.Field(
      'description', column_name=_('description').title()
    )

    class Meta:
        model = models.JobSubtype
        fields = ["name", "job_type", "description"]
    
    # def dehydrate_name(self, obj):