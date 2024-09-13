from __future__ import annotations

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models
from ..base.mixins.filters import FiltersMixins


class JobSubtypeFilterSet(FiltersMixins, filters.FilterSet):

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
                "data-type": "select",
                "type": "search",
                "data-disabled": "",
                "hx-preserve": "",
            }
        ),
    )
    
    class Meta:
        model = models.JobSubtype
        fields = ["name", "job_type", "description"]