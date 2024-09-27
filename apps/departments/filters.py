from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.fields import Object, get_search_input


class DepartmentFilterSet(FiltersMixin, filters.FilterSet):

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
    cost_center = filters.ModelMultipleChoiceFilter(
        queryset=models.cc_models.CostCenter.objects.all(),
        field_name='cost_center',
        lookup_expr='in',
        label=_('cost center'),
        method="filter_combobox",
    )
    parent = filters.ModelMultipleChoiceFilter(
        queryset=models.cc_models.CostCenter.objects.all(),
        field_name='parent',
        lookup_expr='in',
        label=_('department'),
        method="filter_combobox",
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

        cost_center = Object(
            url_name='cost_centers:search', 
            field_name='cost_center', 
            model=models.cc_models.CostCenter,
            value_attributes=['name'],
            multiple=True,
        )
        
        self.form.fields['cost_center'].widget = get_search_input(
            widget=widgets.SelectMultiple,
            form=self.form, 
            obj=cost_center,
        )

        parent = Object(
            url_name='departments:search', 
            field_name='parent', 
            model=models.Department,
            value_attributes=['name'],
            multiple=True,
        )
        
        self.form.fields['parent'].widget = get_search_input(
            widget=widgets.SelectMultiple,
            form=self.form, 
            obj=parent,
        )

    class Meta:
        model = models.Department
        fields = ["name", "cost_center", "parent"]
