from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.base.widgets import ComboboxWidget
from apps.base.mixins.filters import FiltersMixin


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
    job_type = filters.ModelMultipleChoiceFilter(
        queryset=models.JobType.objects.all(),
        field_name='job_type',
        lookup_expr='in',
        label=_('job type'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('job type')})
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
        fields = ["name", "job_type", "description"]