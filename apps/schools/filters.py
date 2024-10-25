from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.nationalities.models import Nationality
from apps.school_types.models import SchoolType
from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.filters import get_combobox_filters


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
    nationality, nationality_reversed = get_combobox_filters(
        qs=Nationality.objects.all(),
        field_name='nationality',
        label=_('nationality'),
    )
    school_type, school_type_reversed = get_combobox_filters(
        qs=SchoolType.objects.all(),
        field_name='school_type',
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
