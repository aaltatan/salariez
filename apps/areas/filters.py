from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models
from ..base.mixins.filters import FiltersMixin
from apps.base.utils import get_search_input, Object


class AreaFilterSet(FiltersMixin, filters.FilterSet):

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
                "type": "search",
                "data-disabled": "",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        city = Object(
            url_name='cities:search', 
            field_name='city', 
            model=models.City,
            value_attributes=['name'],
        )
        
        self.form.fields['city'].widget = get_search_input(
            widget=widgets.TextInput,
            form=self.form, 
            obj=city,
        )

    class Meta:
        model = models.Area
        fields = ["name", "city", "description"]
