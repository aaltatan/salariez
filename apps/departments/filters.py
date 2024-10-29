from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.base.widgets import ComboboxWidget
from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.filters import get_combobox_choices_filter

class DepartmentFilterSet(FiltersMixin, filters.FilterSet):

    class LevelChoices(models.models.TextChoices):
        NONE = '', _('level').title()
        ZERO = '0', '0'
        ONE = '1', '1'
        TWO = '2', '2'
        THREE = '3', '3'
        FOUR = '4', '4'
        FIVE = '5', '5'
        SIX = '6', '6'

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
    cost_center = get_combobox_choices_filter(
        model=models.Department,
        field_name='cost_center__name',
        label=_('cost center'),
    )
    parent = filters.ModelMultipleChoiceFilter(
        queryset=models.Department.objects.all(),
        field_name='parent',
        lookup_expr='in',
        label=_('parent'),
        method="filter_parent",
        widget=ComboboxWidget({'data-name': _('parent')}),
    )
    level = filters.NumberFilter(label=_('level'))
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.form.fields['level'].default = self.LevelChoices.NONE
        self.form.fields['level'].widget = widgets.Select(
            {'placeholder': _('select level')},
            choices=self.LevelChoices.choices
        )

    class Meta:
        model = models.Department
        fields = ["name", "parent"]
