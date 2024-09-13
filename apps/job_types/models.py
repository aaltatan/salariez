from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models.signals import pre_save

from apps.base import (
    models as base_models,
    managers,
    utils,
)

class JobType(base_models.AbstractNameModel):

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
        return reverse('job_types:create')
    
    @property
    def get_update_path(self):
        return reverse('job_types:update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_path(self):
        return reverse('job_types:delete', kwargs={'slug': self.slug})
    
    def __str__(self) -> str:
        return self.name


def job_type_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(job_type_pre_save, JobType)