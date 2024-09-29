from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models
from ..base.mixins.filters import FiltersMixin


class EmployeeFilterSet(FiltersMixin, filters.FilterSet):

    firstname = filters.CharFilter(
        label=_('firstname'),
        method="filter_name",
        widget=widgets.TextInput(
            attrs={
                "autocomplete": "off",
                "placeholder": _("search by the firstname"),
                "type": "search",
                "data-disabled": "",
            }
        ),
    )

    class Meta:
        model = models.Employee
        fields = ["firstname"]
