from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.base import validators, utils
from apps.base.models import AbstractNameModel


class CostCenter(AbstractNameModel):
    
    cost_center_accounting_id = models.CharField(
      verbose_name=_('cost center id'),
      validators=[validators.numeric_validator],
      unique=True,
      help_text=_('cost center id in accounting system'),
      max_length=10,
    )
    
    class Meta:
        ordering = ['name']
        permissions = [
            ['can_export', 'Can export data']
        ]


def cost_center_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(cost_center_pre_save, CostCenter)