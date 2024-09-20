from __future__ import annotations

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models
from ..base.mixins.filters import FiltersMixin


class JobSubtypeFilterSet(FiltersMixin, filters.FilterSet):

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
    description = filters.CharFilter(
        label=_('description'),
        method="filter_description",
        widget=widgets.TextInput(
            attrs={
                "autocomplete": "off",
                "placeholder": _("search by the description"),
                "data-type": "select",
                "type": "search",
                "data-disabled": "",
            }
        ),
    )
    
    class Meta:
        model = models.JobSubtype
        fields = ["name", "job_type", "description"]