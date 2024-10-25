from django.utils.translation import gettext_lazy as _

import django_filters as filters

from . import models

from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.filters import (
    get_date_filters,
    get_number_filters,
    get_combobox_filters
)


class ExchangeRateFilterSet(FiltersMixin, filters.FilterSet):

    currency, currency_reversed = get_combobox_filters(
        qs=models.Currency.objects.all(),
        field_name='currency',
        label=_('currency'),
    )
    date_from, date_to = get_date_filters('date')
    rate_from, rate_to = get_number_filters('rate')

    class Meta:
        model = models.ExchangeRate
        fields = [
            "bulletin_number",
        ]
