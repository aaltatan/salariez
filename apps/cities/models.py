from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.base import models as base_models, utils


class City(base_models.AbstractNameModel):

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'cities'
        permissions = [
            ['can_export', 'Can export data']
        ]


def city_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(city_pre_save, City)