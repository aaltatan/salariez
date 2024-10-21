from django.utils.translation import gettext_lazy as _

import django_filters as filters

from . import models
from apps.base.widgets import ComboboxWidget
from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.filters import (
    get_date_filters,
    get_number_filters,
)


class ExchangeRateFilterSet(FiltersMixin, filters.FilterSet):

    currency = filters.ModelMultipleChoiceFilter(
        queryset=models.Currency.objects.all(),
        field_name='currency',
        lookup_expr='in',
        label=_('currency'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('currency')}),
    )

    date_from, date_to = get_date_filters('date')
    rate_from, rate_to = get_number_filters('rate')

    class Meta:
        model = models.ExchangeRate
        fields = [
            "bulletin_number",
        ]
