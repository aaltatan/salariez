from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models
from ..base.mixins.filters import FiltersMixins


class PositionFilterSet(FiltersMixins, filters.FilterSet):

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

    class Meta:
        model = models.Position
        fields = ["name", "description"]
