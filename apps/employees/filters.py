from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.job_types.models import JobType
from apps.job_subtypes.models import JobSubtype
from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.fields import (
    get_search_field, Object
)


class EmployeeFilterSet(FiltersMixin, filters.FilterSet):

    firstname = filters.CharFilter(
        label=_('fullname'),
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
    job_status = filters.ModelMultipleChoiceFilter(
        queryset=models.employee.Status.objects.all(),
        field_name='job_status',
        lookup_expr='in',
        label=_('job status'),
        method="filter_combobox",
    )
    job_type = filters.ModelMultipleChoiceFilter(
        queryset=JobType.objects.all(),
        field_name='job_subtype__job_type',
        lookup_expr='in',
        label=_('job type'),
        method="filter_combobox",
    )
    job_subtype = filters.ModelMultipleChoiceFilter(
        queryset=JobSubtype.objects.all(),
        field_name='job_subtype',
        lookup_expr='in',
        label=_('job subtype'),
        method="filter_combobox",
    )


    def __init__(
        self, data=None, queryset=None, *, request=None, prefix=None
    ):
        super().__init__(data, queryset, request=request, prefix=prefix)

        job_status = Object(
            url_name='statuses:search', 
            field_name='job_status', 
            model=models.employee.Status,
            value_attributes=['name'],
            multiple=True,
        )
        self.form.fields['job_status'].widget = get_search_field(
            widget=widgets.SelectMultiple, form=self.form, obj=job_status
        )

        job_type = Object(
            url_name='job_types:search', 
            field_name='job_type', 
            model=JobType,
            value_attributes=['name'],
            multiple=True,
        )
        self.form.fields['job_type'].widget = get_search_field(
            widget=widgets.SelectMultiple, form=self.form, obj=job_type
        )

        job_subtype = Object(
            url_name='job_subtypes:search', 
            field_name='job_subtype', 
            model=JobSubtype,
            value_attributes=['name'],
            multiple=True,
        )
        self.form.fields['job_subtype'].widget = get_search_field(
            widget=widgets.SelectMultiple, form=self.form, obj=job_subtype
        )

    class Meta:
        model = models.Employee
        fields = ["firstname", "job_status", "status", "gender"]