from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models.signals import pre_save

from apps.base import validators, utils
from apps.base.models import AbstractNameModel
from apps.base.managers import SearchManager


class CostCenter(AbstractNameModel):
    
    cost_center_accounting_id = models.CharField(
      verbose_name=_('cost center id'),
      validators=[validators.numeric_validator],
      unique=True,
      help_text=_('cost center id in accounting system'),
      max_length=10,
    )
    
    objects = SearchManager()
    
    class Meta:
        ordering = ['name']
        permissions = [
            ['can_export', 'Can export data']
        ]
    
    @property
    def get_create_path(self):
        return reverse('cost_centers:create')
    
    @property
    def get_update_path(self):
        return reverse(
          'cost_centers:update', kwargs={'slug': self.slug}
        )
    
    @property
    def get_delete_path(self):
        return reverse(
          'cost_centers:delete', kwargs={'slug': self.slug}
        )
    
    def __str__(self) -> str:
        return self.name


def cost_center_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(cost_center_pre_save, CostCenter)