from django.db import models
from django.db.models import When, Case, Q, Value, F
from django.db.models.fields.generated import GeneratedField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.currencies.models import Currency


class ExchangeRate(models.Model):

    currency = models.ForeignKey(
        Currency, related_name='rates', on_delete=models.PROTECT
    )
    input_rate = models.DecimalField(
        max_digits=28, decimal_places=8
    )
    is_inverse = models.BooleanField(default=False)
    rate = GeneratedField(
        expression=Case(
            When(
                Q(is_inverse__exact=True), then=Value(1) / F('input_rate')
            ),
            default=F('input_rate'),
        ),
        output_field=models.DecimalField(max_digits=28, decimal_places=8),
        db_persist=False,
    )
    date = models.DateField(default=timezone.now)
    bulletin_number = models.CharField(
        max_length=255, 
        unique=True,
        help_text=_('bulletin number from central bank')
    )
    notes = models.TextField(max_length=1000, default='', blank=True)

    @property
    def get_delete_path(self):
        return reverse('exchange_rates:delete', kwargs={'pk': self.pk})

    @property
    def get_update_path(self):
        return reverse('exchange_rates:update', kwargs={'pk': self.pk})

    @property
    def get_create_path(self):
        return reverse('exchange_rates:create')

    def __str__(self) -> str:
        str_date = self.date.strftime('%Y-%m-%d')
        return f'{self.currency.name} - {self.rate} / {str_date}'
    
    class Meta:
        ordering = ['-date', 'currency__name']
        unique_together = [
            ('currency', 'date')
        ]
        permissions = [
            ['can_export', 'Can export data']
        ]