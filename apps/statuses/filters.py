from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models
from ..base.mixins.filters import FiltersMixin


class StatusFilterSet(FiltersMixin, filters.FilterSet):
    
    advanced_search = filters.CharFilter(
        method='filter_djangoql', 
        label=_('advanced search'),
        widget=widgets.TextInput({
            "placeholder": _("search by djangoQL"),
        })
    )
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
    has_salary = filters.ChoiceFilter(
        label=_('has salary'),
        choices=models.HAS_SALARY_CHOICES
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
        model = models.Status
        fields = ["name", "has_salary", "description"]
