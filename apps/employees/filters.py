from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from . import models

from apps.departments.models import Department
from apps.positions.models import Position
from apps.job_types.models import JobType
from apps.job_subtypes.models import JobSubtype
from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.filters import (
    get_decimal_filters, 
    get_date_filters,
    get_number_filters
)
from apps.base.utils.fields import (
    get_search_field,
    Object
)


class EmployeeFilterSet(FiltersMixin, filters.FilterSet):

    firstname = filters.CharFilter(
        label=_('fullname'),
        method="filter_name",
        widget=widgets.TextInput({
            "autocomplete": "off",
            "placeholder": _("search by the name"),
            "type": "search",
            "data-disabled": "",
        }),
    )
    job_status = filters.ModelMultipleChoiceFilter(
        queryset=models.employee.Status.objects.all(),
        field_name='job_status',
        label=_('job status'),
        method="filter_combobox",
    )
    job_type = filters.ModelMultipleChoiceFilter(
        queryset=JobType.objects.all(),
        field_name='job_subtype__job_type',
        label=_('job type'),
        method="filter_combobox",
    )
    job_subtype = filters.ModelMultipleChoiceFilter(
        queryset=JobSubtype.objects.all(),
        field_name='job_subtype',
        label=_('job subtype'),
        method="filter_combobox",
    )
    position = filters.ModelMultipleChoiceFilter(
        queryset=Position.objects.all(),
        field_name='position',
        label=_('position'),
        method="filter_combobox",
    )
    department = filters.ModelMultipleChoiceFilter(
        queryset=Department.objects.all(),
        field_name='department',
        label=_('department'),
        method="filter_parent",
    )

    salary_gte, salary_lte = get_decimal_filters('salary')
    job_age_gte, job_age_lte = get_number_filters('job_age')
    age_gte, age_lte = get_number_filters('age')
    hire_date_gte, hire_date_lte = get_date_filters('hire_date')

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
            widget=widgets.SelectMultiple, 
            form=self.form, 
            obj=job_status
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
            widget=widgets.SelectMultiple, 
            form=self.form, 
            obj=job_subtype
        )

        position = Object(
            url_name='positions:search', 
            field_name='position', 
            model=Position,
            value_attributes=['name'],
            multiple=True,
        )
        self.form.fields['position'].widget = get_search_field(
            widget=widgets.SelectMultiple, form=self.form, obj=position
        )

        department = Object(
            url_name='departments:search', 
            field_name='department', 
            model=Department,
            value_attributes=['name'],
            multiple=True,
        )
        self.form.fields['department'].widget = get_search_field(
            widget=widgets.SelectMultiple, form=self.form, obj=department
        )

    class Meta:
        model = models.Employee
        fields = ["firstname", "status", "gender"]