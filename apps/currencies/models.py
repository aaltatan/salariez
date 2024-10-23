from django.db import models
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _

from apps.base import models as base_models, utils


IS_LOCAL_CHOICES = (
    (False, _('foreign').title()),
    (True, _('local').title()),
)

class CurrencyManager(models.Manager):

    def get_queryset(self) -> models.QuerySet:

        from apps.exchange_rates.models import ExchangeRate

        rates = ExchangeRate.objects.filter(
            currency=OuterRef('pk')
        ).order_by('date', 'pk')

        return (
            super().get_queryset().annotate(
                rate=Coalesce(
                    Subquery(rates.values('rate')[:1]), 
                    Value(1),
                    output_field=models.DecimalField(
                        max_digits=20,
                        decimal_places=8,
                    )
                ),
                date=Coalesce(
                    Subquery(rates.values('date')[:1]),
                    Value('-'),
                    output_field=models.CharField()
                ),
            )
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

    objects = CurrencyManager()

    @classmethod
    def get_default_pk(cls):
        currency, created = cls.objects.get_or_create(
            is_local=True,
            defaults={
                'name': 'Syrian Pound',
                'short_name': 's.p.',
                'fraction_name': 'Korsh',
                'is_local': True
            }
        )
        return currency.pk

    class Meta:
        ordering = ['is_local', 'name']
        verbose_name_plural = 'currencies'
        permissions = [
            ['can_export', 'Can export data']
        ]
    
    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        # if self.is_local:
        #     raise Exception(
        #         'cannot delete local currency'
        #     )
        return super().delete(*args, **kwargs)

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