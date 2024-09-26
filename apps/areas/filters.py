from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.base.mixins.filters import FiltersMixin
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
    city = filters.ModelMultipleChoiceFilter(
        queryset=models.City.objects.all(),
        field_name='city',
        lookup_expr='in',
        label=_('city'),
        method="filter_city",
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

    def filter_city(self, qs, name, value):
        if not value:
            return qs
        return qs.filter(city__in=value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        city = Object(
            url_name='cities:search', 
            field_name='city', 
            model=models.City,
            value_attributes=['name'],
            multiple=True,
        )
        
        self.form.fields['city'].widget = get_search_input(
            widget=widgets.SelectMultiple,
            form=self.form, 
            obj=city,
        )

    class Meta:
        model = models.Area
        fields = ["name", "city", "description"]
