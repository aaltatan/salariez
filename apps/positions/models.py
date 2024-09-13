from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models.signals import pre_save

from apps.base import (
    models as base_models,
    managers,
    utils,
)

class Position(base_models.AbstractNameModel):

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
        return reverse('positions:create')
    
    @property
    def get_update_path(self):
        return reverse('positions:update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_path(self):
        return reverse('positions:delete', kwargs={'slug': self.slug})
    
    def __str__(self) -> str:
        return self.name


def position_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(position_pre_save, Position)