from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.base import models as base_models, utils
from apps.cities.models import City


class AreaManager(models.Manager):

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('city')


class Area(base_models.AbstractNameModel):

    city = models.ForeignKey(
        City, 
        on_delete=models.PROTECT,
        related_name='areas',
        help_text=_('city'),
        verbose_name=_('city')
    )

    objects = AreaManager()

    class Meta:
        ordering = ['city__name', 'name']
        permissions = [
            ['can_export', 'Can export data']
        ]


def area_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(area_pre_save, Area)