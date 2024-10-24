from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from .models import Employee

from apps.base.widgets import ComboboxWidget

from apps.educational_degrees.models import EducationalDegree
from apps.specializations.models import Specialization
from apps.job_subtypes.models import JobSubtype
from apps.cost_centers.models import CostCenter
from apps.departments.models import Department
from apps.positions.models import Position
from apps.job_types.models import JobType
from apps.statuses.models import Status
from apps.schools.models import School
from apps.groups.models import Group

from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.filters import (
    get_decimal_filters, 
    get_date_filters,
    get_number_filters
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
    status = filters.ModelMultipleChoiceFilter(
        queryset=Status.objects.all(),
        field_name='status_pk',
        label=_('status'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('status')}),
    )
    job_type = filters.ModelMultipleChoiceFilter(
        queryset=JobType.objects.all(),
        field_name='job_type_pk',
        label=_('job type'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('job type')}),
    )
    job_subtype = filters.ModelMultipleChoiceFilter(
        queryset=JobSubtype.objects.all(),
        field_name='job_subtype_pk',
        label=_('job subtype'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('job subtype')}),
    )
    position = filters.ModelMultipleChoiceFilter(
        queryset=Position.objects.all(),
        field_name='position_pk',
        label=_('position'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('position')}),
    )
    department = filters.ModelMultipleChoiceFilter(
        queryset=Department.objects.all(),
        field_name='department_pk',
        label=_('department'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('department')}),
    )
    cost_center = filters.ModelMultipleChoiceFilter(
        queryset=CostCenter.objects.all(),
        field_name='cost_center_pk',
        label=_('cost center'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('cost center')}),
    )
    groups = filters.ModelMultipleChoiceFilter(
        queryset=Group.objects.all(),
        field_name='groups',
        label=_('groups'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('groups')}),
    )
    education_degree = filters.ModelMultipleChoiceFilter(
        queryset=EducationalDegree.objects.all(),
        field_name='education_degree_pk',
        label=_('education degree'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('education degree')}),
    )
    specialization = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='specialization_pk',
        label=_('specialization'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('specialization')}),
    )
    school = filters.ModelMultipleChoiceFilter(
        queryset=School.objects.all(),
        field_name='school_pk',
        label=_('school'),
        method="filter_combobox",
        widget=ComboboxWidget({'data-name': _('school')}),
    )
    specialty = filters.BooleanFilter(
        field_name='is_specialist',
        label=_('specialty'),
        widget=widgets.Select(choices=(
            (None, '---------'),
            (True, _('specialist').title()),
            (False, _('supporter').title()),
        )),
    )

    salary_gte, salary_lte = get_decimal_filters('salary')
    local_salary_gte, local_salary_lte = get_decimal_filters('local_salary')
    job_age_gte, job_age_lte = get_number_filters('job_age')
    age_gte, age_lte = get_number_filters('age')
    hire_date_gte, hire_date_lte = get_date_filters('hire_date')

    class Meta:
        model = Employee
        fields = ["firstname", "gender"]