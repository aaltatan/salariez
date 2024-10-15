from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.base.widgets import ComboboxWidget
from apps.base.mixins.filters import FiltersMixin


class AreaFilterSet(FiltersMixin, filters.FilterSet):

    name = filters.CharFilter(
        label=_('name'),
        method="filter_name",
        widget=widgets.TextInput({
            "autocomplete": "off",
            "placeholder": _("search by the name"),
            "type": "search",
            "data-disabled": "",
        }),
    )
    city = filters.ModelMultipleChoiceFilter(
        queryset=models.City.objects.all(),
        field_name='city',
        lookup_expr='in',
        label=_('city'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('city')}),
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
        model = models.Area
        fields = ["name", "city", "description"]
