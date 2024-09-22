from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.base import models as base_models, utils


HAS_SALARY_CHOICES = (
    (True, _('has salary').title()),
    (False, _('has not salary').title()),
)

class Status(base_models.AbstractNameModel):

    has_salary = models.BooleanField(
        verbose_name=_('has salary'),
        default=False,
        help_text=_('can he has a salary?'),
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'statuses'
        permissions = [
            ['can_export', 'Can export data']
        ]


def status_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(status_pre_save, Status)