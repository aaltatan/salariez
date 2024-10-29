from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.filters import get_combobox_choices_filter


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
    nationality = get_combobox_choices_filter(
        model=models.School,
        field_name='nationality__name',
        label=_('nationality'),
    )
    school_type = get_combobox_choices_filter(
        model=models.School,
        field_name='school_type__name',
        label=_('type'),
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
        fields = ["name", "description"]
