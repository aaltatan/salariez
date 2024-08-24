from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets
from django.urls import reverse_lazy

import django_filters as filters

from . import models
from ..base.mixins.filters import FiltersMixins, ATTRS


class FacultyFilterSet(FiltersMixins, filters.FilterSet):
    
    attrs = {
        **ATTRS,
        **{
            "hx-get": reverse_lazy("faculties:index"),
            "hx-trigger": "input changed delay:500ms, search",
            "placeholder": _("search by the name"),
            "type": "search",
        }
    }

    name = filters.CharFilter(
        label='',
        widget=widgets.TextInput(attrs=attrs),
        method='filter_name',
    )
    
    class Meta:
        model = models.Faculty
        fields = ['name']