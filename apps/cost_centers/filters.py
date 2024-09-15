from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models
from ..base.mixins.filters import FiltersMixin


class CostCenterFilterSet(FiltersMixin, filters.FilterSet):

    name = filters.CharFilter(
        label="",
        method="filter_name",
        widget=widgets.TextInput(
            attrs={
                "autocomplete": "off",
                "placeholder": _("search by the name"),
                "type": "search",
                "data-disabled": "",
                "hx-preserve": "",
            }
        ),
    )
    description = filters.CharFilter(
        label="",
        method="filter_description",
        widget=widgets.TextInput(
            attrs={
                "autocomplete": "off",
                "placeholder": _("search by the description"),
                "type": "search",
                "data-disabled": "",
                "hx-preserve": "",
            }
        ),
    )
    cost_center = filters.CharFilter(
        label="",
        method="filter_cost_center",
        widget=widgets.TextInput(
            attrs={
                "autocomplete": "off",
                "placeholder": _("search by the cost center"),
                "type": "search",
                "x-mask": "999999999",
                "data-disabled": "",
                "hx-preserve": "",
            }
        ),
    )

    class Meta:
        model = models.CostCenter
        fields = ["name", "cost_center", "description"]
