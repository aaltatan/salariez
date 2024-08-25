from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models
from ..base.mixins.filters import FiltersMixins


class FacultyFilterSet(FiltersMixins, filters.FilterSet):

    name = filters.CharFilter(
        label="",
        method="filter_name",
        widget=widgets.TextInput(
            attrs={
                "autocomplete": "off",
                "autofocus": "",
                "placeholder": _("search by the name"),
                "type": "search",
                "data-disabled": "",
            }
        ),
    )

    class Meta:
        model = models.Faculty
        fields = ["name"]
