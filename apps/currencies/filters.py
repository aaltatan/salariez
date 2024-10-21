from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models
from ..base.mixins.filters import FiltersMixin


class CurrencyFilterSet(FiltersMixin, filters.FilterSet):

    name = filters.CharFilter(
        label=_('name'),
        method="filter_name",
        widget=widgets.TextInput(
            attrs={
                "autocomplete": "off",
                "placeholder": _("search by the name"),
                "type": "search",
                "data-disabled": "",
            }
        ),
    )
    short_name = filters.CharFilter(
        label=_('short name'),
        field_name='short_name',
        lookup_expr='contains',
        widget=widgets.TextInput(
            attrs={
                "autocomplete": "off",
                "placeholder": _("search by the short name"),
            }
        ),
    )
    fraction_name = filters.CharFilter(
        label=_('fraction'),
        field_name='fraction_name',
        lookup_expr='contains',
        widget=widgets.TextInput(
            attrs={
                "autocomplete": "off",
                "placeholder": _("search by the short name"),
            }
        ),
    )
    is_local = filters.ChoiceFilter(
        label=_('locality'),
        choices=models.IS_LOCAL_CHOICES
    )
    description = filters.CharFilter(
        label=_('description'),
        method="filter_description",
        widget=widgets.TextInput({
            "autocomplete": "off",
            "placeholder": _("search by the description"),
            "type": "search",
            "data-disabled": "",
        }),
    )

    class Meta:
        model = models.Currency
        fields = [
            'name', 
            'short_name', 
            'fraction_name', 
            'is_local', 
            'description',
        ]
