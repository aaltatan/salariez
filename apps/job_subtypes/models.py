from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.job_types.models import JobType
from apps.base import models as base_models, utils


class JobSubType(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('job_type')


class JobSubtype(base_models.AbstractNameModel):
    
    job_type = models.ForeignKey(
        JobType, 
        on_delete=models.PROTECT,
        related_name='subtypes',
        help_text=_('primary job type'),
        verbose_name=_('job type')
    )

    objects = JobSubType()

    class Meta:
        ordering = ['name']
        permissions = [
            ['can_export', 'Can export data']
        ]


def job_subtype_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(job_subtype_pre_save, JobSubtype)