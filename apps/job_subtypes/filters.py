from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.base.mixins.filters import FiltersMixin
from apps.base.utils import get_search_input, Object


class JobSubtypeFilterSet(FiltersMixin, filters.FilterSet):

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
    job_type = filters.ModelMultipleChoiceFilter(
        queryset=models.JobType.objects.all(),
        field_name='job_type',
        lookup_expr='in',
        label=_('job type'),
        method="filter_combobox",
    )
    description = filters.CharFilter(
        label=_('description'),
        method="filter_description",
        widget=widgets.TextInput(
            attrs={
                "autocomplete": "off",
                "placeholder": _("search by the description"),
                "data-type": "select",
                "type": "search",
                "data-disabled": "",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        job_type = Object(
            url_name='job_types:search', 
            field_name='job_type', 
            model=models.JobType,
            value_attributes=['name'],
            multiple=True,
        )
        
        self.form.fields['job_type'].widget = get_search_input(
            widget=widgets.SelectMultiple,
            form=self.form, 
            obj=job_type,
        )

    class Meta:
        model = models.JobSubtype
        fields = ["name", "job_type", "description"]