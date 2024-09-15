from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models
from ..base.mixins.filters import FiltersMixin


class FacultyFilterSet(FiltersMixin, filters.FilterSet):

    name = filters.CharFilter(
        label="",
        method="filter_name",
        widget=widgets.TextInput(
            attrs={
                "autocomplete": "off",
                "autofocus": "on",
                "placeholder": _("search by the name"),
                "type": "search",
                "data-disabled": "",
                "hx-preserve": "",
            }
        ),
    )

    class Meta:
        model = models.Faculty
        fields = ["name"]
