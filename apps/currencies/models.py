from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from apps.base import models as base_models, utils


IS_LOCAL_CHOICES = (
    (False, _('foreign').title()),
    (True, _('local').title()),
)

class Currency(base_models.AbstractNameModel):

    short_name = models.CharField(
        max_length=10,
        verbose_name=_('short name'),
    )
    fraction_name = models.CharField(
        max_length=20,
        verbose_name=_('fraction name'),
    )
    is_local = models.BooleanField(
        verbose_name=_('is local'),
        default=False,
        help_text=_('is it local or foreign?'),
    )

    class Meta:
        ordering = ['is_local', 'name']
        verbose_name_plural = 'currencies'
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


def currency_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)


pre_save.connect(currency_pre_save, Currency)