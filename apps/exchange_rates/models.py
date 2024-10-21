from uuid import uuid4

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.currencies.models import Currency


class ExchangeRate(models.Model):

    currency = models.ForeignKey(
        Currency, related_name='rates', on_delete=models.PROTECT
    )
    input_rate = models.DecimalField(
        max_digits=20, decimal_places=8
    )
    is_inverse = models.BooleanField(default=False)
    rate = models.DecimalField(
        max_digits=20, decimal_places=8
    )
    date = models.DateField(default=timezone.now)
    bulletin_number = models.CharField(
        max_length=255, 
        unique=True,
        help_text=_('bulletin number from central bank')
    )
    notes = models.TextField(max_length=1000, default='', blank=True)
    slug = models.SlugField(
        unique=True,
        max_length=255,
        allow_unicode=True,
        null=True,
        blank=True,
    )

    def _get_app_label(self):
        return self.__class__._meta.app_label
    
    @property
    def get_delete_path(self):
        return reverse(
            'exchange_rates:delete', kwargs={'slug': self.slug}
        )

    @property
    def get_update_path(self):
        return reverse(
            'exchange_rates:update', kwargs={'slug': self.slug}
        )

    @property
    def get_create_path(self):
        return reverse('exchange_rates:create')

    @property
    def get_activity_path(self):
        kwargs = {
            'app_label': self._get_app_label(),
            'model_name': self.__class__.__name__,
            'object_id': self.id,
        }
        return reverse('activities:index', kwargs=kwargs)
    
    @property
    def get_contextmenu_path(self):
        return reverse(
            f'{self._get_app_label()}:index', kwargs={'id': self.pk}
        )
    
    def __str__(self) -> str:
        str_date = self.date.strftime('%Y-%m-%d')
        return f'{self.currency.name} / {str_date}'
    
    class Meta:
        ordering = ['-date', 'currency__name']
        unique_together = [
            ('currency', 'date')
        ]
        permissions = [
            ['can_export', 'Can export data']
        ]


def exchange_rate_pre_save(
    sender, instance: ExchangeRate, *args, **kwargs
) -> None:
    
    if instance.currency.is_local:
        instance.is_inverse = False
        instance.input_rate = 1

    if instance.is_inverse:
        instance.rate = 1 / instance.input_rate
    else:
        instance.rate = instance.input_rate

    if instance.slug is None:
        instance.slug = str(uuid4())


pre_save.connect(exchange_rate_pre_save, ExchangeRate)