from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.job_types.models import JobType
from apps.job_subtypes.models import JobSubtype
from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.generic import parse_decimals
from apps.base.utils.fields import (
    get_search_field,
    get_date_field, 
    Object
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
    salary_gte = filters.CharFilter(
        field_name='salary__gte',
        label=_('salary from'),
        method="filter_salary",
        widget=widgets.TextInput({
            'x-mask:dynamic': '$money($input)'
        })
    )
    salary_lte = filters.CharFilter(
        field_name='salary__lte',
        label=_('salary to'),
        method="filter_salary",
        widget=widgets.TextInput({
            'x-mask:dynamic': '$money($input)'
        })
    )
    # hire_date_gte = filters.CharFilter(
    #     field_name='hire_date__gte',
    #     label=_('hire date from'),
    #     method="filter_hire_date",
    #     widget=get_date_field()
    # )
    # hire_date_lte = filters.CharFilter(
    #     field_name='hire_date__lte',
    #     label=_('hire date to'),
    #     method="filter_hire_date",
    #     widget=get_date_field()
    # )
    age_gte = filters.NumberFilter(
        field_name='age__gte',
        label=_('age from'),
        method="filter_age",
    )
    age_lte = filters.NumberFilter(
        field_name='age__lte',
        label=_('age to'),
        method="filter_age",
    )

    def filter_salary(self, qs, name, value):
        if value:
            lookup = {name: parse_decimals(value)}
            return qs.filter(**lookup)
        return qs

    def filter_hire_date(self, qs, name, value):
        if value:
            lookup = {name: value}
            return qs.filter(**lookup)
        return qs

    def filter_age(self, qs, name, value):
        if value:
            lookup = {name: value}
            return qs.filter(**lookup)
        return qs


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