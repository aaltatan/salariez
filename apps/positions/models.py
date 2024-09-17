from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.base import models as base_models, utils


class Position(base_models.AbstractNameModel):

    class Meta:
        ordering = ['name']
        permissions = [
            ['can_export', 'Can export data']
        ]


def position_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(position_pre_save, Position)