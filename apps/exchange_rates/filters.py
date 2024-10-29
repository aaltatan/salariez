from django.utils.translation import gettext_lazy as _

import django_filters as filters

from . import models

from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.filters import (
    get_date_filters,
    get_number_filters,
    get_combobox_choices_filter,
)


class ExchangeRateFilterSet(FiltersMixin, filters.FilterSet):

    currency = get_combobox_choices_filter(
        model=models.ExchangeRate,
        field_name='currency__name',
        label=_('currency'),
    )
    date_from, date_to = get_date_filters('date')
    rate_from, rate_to = get_number_filters('rate')

    class Meta:
        model = models.ExchangeRate
        fields = [
            "bulletin_number",
        ]
