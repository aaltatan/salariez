from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models.signals import pre_save

from apps.currencies.models import Currency


class ExchangeRate(models.Model):

    currency = models.ForeignKey(
        Currency, related_name='rates', on_delete=models.PROTECT
    )
    input_rate = models.DecimalField(
        max_digits=12, decimal_places=8
    )
    rate = models.DecimalField(
        max_digits=12, decimal_places=8
    )
    is_inverse = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    bulletin_number = models.CharField(
        max_length=255, 
        unique=True,
        help_text=_('bulletin number from central bank')
    )
    notes = models.TextField(max_length=1000, default='')

    def __str__(self) -> str:
        str_date = self.date.strftime('%Y-%m-%d')
        return f'{self.currency.name} - {self.rate} / {str_date}'
    
    class Meta:
        ordering = ['-date']
        unique_together = [
            ('currency', 'date')
        ]
        permissions = [
            ['can_export', 'Can export data']
        ]


def exchange_rate_pre_save(
    sender, instance: ExchangeRate, *args, **kwargs
):
    if instance.is_inverse:
        instance.rate = 1 / instance.input_rate
    else:
        instance.rate = instance.input_rate


pre_save.connect(exchange_rate_pre_save, ExchangeRate)