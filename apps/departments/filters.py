from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.fields import Object, get_search_input


class DepartmentFilterSet(FiltersMixin, filters.FilterSet):

    class LevelChoices(models.models.TextChoices):
        NONE = '', _('select level')
        ZERO = '0', '0'
        ONE = '1', '1'
        TWO = '2', '2'
        THREE = '3', '3'
        FOUR = '4', '4'
        FIVE = '5', '5'
        SIX = '6', '6'

    class TypeChoices(models.models.TextChoices):
        NONE = '', _('select type')
        PRIMARY = 'primary', _('primary')
        PARTIAL = 'partial', _('partial')


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
    cost_center = filters.ModelMultipleChoiceFilter(
        queryset=models.cc_models.CostCenter.objects.all(),
        field_name='cost_center',
        lookup_expr='in',
        label=_('cost center'),
        method="filter_combobox",
    )
    parent = filters.ModelMultipleChoiceFilter(
        queryset=models.Department.objects.all(),
        field_name='parent',
        lookup_expr='in',
        label=_('parent'),
        method="filter_parent",
    )
    level = filters.NumberFilter(label=_('level'))
    type = filters.CharFilter(label=_('type'), method='filter_primary')
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

    def filter_parent(self, qs, name, value):

        if not value:
            return qs
        
        stmt = qs.none()
        for obj in value:
            stmt = obj.get_descendants() | stmt

        return stmt

    def filter_primary(self, qs, name, value):

        stmt = qs.none()

        for obj in qs:
            if value == 'primary':
                if obj.is_leaf_node():
                    stmt = obj | stmt
            else:
                if not obj.is_leaf_node():
                    stmt = obj | stmt

        return stmt

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
        
        self.form.fields['level'].default = self.LevelChoices.NONE
        self.form.fields['level'].widget = widgets.Select(
            {'placeholder': _('select level')},
            choices=self.LevelChoices.choices
        )
        
        self.form.fields['type'].default = self.TypeChoices.NONE
        self.form.fields['type'].widget = widgets.Select(
            {'placeholder': _('select type')},
            choices=self.TypeChoices.choices
        )

    class Meta:
        model = models.Department
        fields = ["name", "cost_center", "parent"]
