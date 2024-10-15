from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.base import models as base_models, utils


IS_SPECIALIST_CHOICES = (
    (False, _('supporter').title()),
    (True, _('specialist').title()),
)


class Specialization(base_models.AbstractNameModel):

    is_specialist = models.BooleanField(
        verbose_name=_('is specialist'),
        default=False,
        help_text=_('is it specialist?'),
    )

    class Meta:
        ordering = ['is_specialist', 'name']
        permissions = [
            ['can_export', 'Can export data']
        ]


def specialization_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(specialization_pre_save, Specialization)