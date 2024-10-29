from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.filters import get_combobox_choices_filter

class JobSubtypeFilterSet(FiltersMixin, filters.FilterSet):

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
    job_type = get_combobox_choices_filter(
        model=models.JobSubtype,
        field_name='job_type__name',
        label=_('job type'),
    )
    description = filters.CharFilter(
        label=_('description'),
        method="filter_description",
        widget=widgets.TextInput({
            "autocomplete": "off",
            "placeholder": _("search by the description"),
            "data-type": "select",
            "type": "search",
            "data-disabled": "",
        }),
    )

    class Meta:
        model = models.JobSubtype
        fields = ["name", "description"]