from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.base import models as base_models, utils


IS_ACADEMIC_CHOICES = (
    (False, _('applied').title()),
    (True, _('academic').title()),
)


class EducationalDegree(base_models.AbstractNameModel):

    is_academic = models.BooleanField(
        verbose_name=_('is academic'),
        default=False,
        help_text=_('is it academic?'),
    )
    order = models.IntegerField(
        verbose_name=_('order'),
        help_text=_('order of degree'),
        default=1,
    )

    class Meta:
        ordering = ['order', 'is_academic', 'name']
        permissions = [
            ['can_export', 'Can export data']
        ]


def educational_degree_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(educational_degree_pre_save, EducationalDegree)