from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models.signals import pre_save

from apps.job_types.models import JobType
from apps.base import (
    models as base_models,
    managers,
    utils,
)

class JobSubtype(base_models.AbstractNameModel):
    
    job_type = models.ForeignKey(
        JobType, 
        on_delete=models.PROTECT,
        related_name='subtypes',
        help_text=_('primary job type'),
        verbose_name=_('job type')
    )

    def __str__(self) -> str:
        return self.name

    objects = managers.SearchManager()
    
    class Meta:
        ordering = ['name']
        permissions = [
            ['can_export', 'Can export data']
        ]
    
    @property
    def get_create_path(self):
        return reverse('job_subtypes:create')
    
    @property
    def get_update_path(self):
        return reverse('job_subtypes:update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_path(self):
        return reverse('job_subtypes:delete', kwargs={'slug': self.slug})
    
    def __str__(self) -> str:
        return self.name


def job_subtype_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(job_subtype_pre_save, JobSubtype)