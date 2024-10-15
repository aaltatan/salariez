from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.base import models as base_models, utils
from apps.school_types.models import SchoolType
from apps.nationalities.models import Nationality


class School(base_models.AbstractNameModel):

    school_type = models.ForeignKey(
        SchoolType, 
        on_delete=models.PROTECT,
        related_name='schools', 
        help_text=_('school type'),
        verbose_name=_('school type'),
    )
    nationality = models.ForeignKey(
        Nationality, 
        on_delete=models.PROTECT,
        related_name='schools', 
        help_text=_('nationality'),
        verbose_name=_('nationality'),
    )

    class Meta:
        ordering = ['school_type', 'nationality__is_local', 'name']
        permissions = [
            ['can_export', 'Can export data']
        ]


def school_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(school_pre_save, School)