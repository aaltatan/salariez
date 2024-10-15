from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.nationalities.models import Nationality
from apps.school_types.models import SchoolType
from apps.base.mixins.filters import FiltersMixin
from apps.base.widgets import ComboboxWidget


class SchoolFilterSet(FiltersMixin, filters.FilterSet):

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
    nationality = filters.ModelMultipleChoiceFilter(
        queryset=Nationality.objects.all(),
        field_name='nationality',
        lookup_expr='in',
        label=_('nationality'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('nationality')}),
    )
    school_type = filters.ModelMultipleChoiceFilter(
        queryset=SchoolType.objects.all(),
        field_name='school_type',
        lookup_expr='in',
        label=_('type'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('school type')}),
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

    class Meta:
        model = models.School
        fields = ["name", "nationality", "school_type", "description"]
