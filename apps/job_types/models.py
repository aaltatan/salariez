from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.base import models as base_models, utils


class JobType(base_models.AbstractNameModel):

    class Meta:
        ordering = ['name']
        permissions = [
            ['can_export', 'Can export data']
        ]


def job_type_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(job_type_pre_save, JobType)