from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.base import models as base_models, utils


class Nationality(base_models.AbstractNameModel):

    is_local = models.BooleanField(
        verbose_name=_('is local'),
        default=False,
        help_text=_('is it local?'),
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'nationalities'
        permissions = [
            ['can_export', 'Can export data']
        ]
    
    def save(self, *args, **kwargs) -> None:

        if self.is_local:
            Klass = self.__class__
            for obj in Klass.objects.all():
                obj.is_local = False
                obj.save()
            self.is_local = True

        return super().save(*args, **kwargs)


def nationality_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(nationality_pre_save, Nationality)