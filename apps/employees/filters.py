from django.utils.translation import gettext_lazy as _
from django.forms import widgets

import django_filters as filters

from .models import Employee

from apps.base.mixins.filters import FiltersMixin
from apps.base.utils.filters import (
    get_decimal_filters,
    get_date_filters,
    get_number_filters,
    get_combobox_choices_filter,
)


class EmployeeFilterSet(FiltersMixin, filters.FilterSet):

    firstname = filters.CharFilter(
        label=_("fullname"),
        method="filter_name",
        widget=widgets.TextInput(
            {
                "autocomplete": "off",
                "placeholder": _("search by the name"),
                "type": "search",
                "data-disabled": "",
            }
        ),
    )
    status = get_combobox_choices_filter(
        model=Employee,
        field_name='status',
        label=_("status")
    )
    job_type = get_combobox_choices_filter(
        model=Employee,
        field_name='job_type',
        label=_("job type")
    )
    job_subtype = get_combobox_choices_filter(
        model=Employee,
        field_name='job_subtype',
        label=_("job subtype")
    )
    position = get_combobox_choices_filter(
        model=Employee,
        field_name='position',
        label=_("position")
    )
    department = get_combobox_choices_filter(
        model=Employee,
        field_name='department',
        label=_("department")
    )
    cost_center = get_combobox_choices_filter(
        model=Employee,
        field_name='cost_center',
        label=_("cost center")
    )
    groups = get_combobox_choices_filter(
        model=Employee,
        field_name='groups__name',
        label=_("groups")
    )
    offices = get_combobox_choices_filter(
        model=Employee,
        field_name='civil_registry_office',
        label=_("offices")
    )
    registry = get_combobox_choices_filter(
        model=Employee,
        field_name='registry_office_name',
        label=_("registry")
    )
    education_degree = get_combobox_choices_filter(
        model=Employee,
        field_name='education_degree',
        label=_("education degree"),
    )
    specialization = get_combobox_choices_filter(
        model=Employee,
        field_name='specialization',
        label=_("specialization"),
    )
    nationality = get_combobox_choices_filter(
        model=Employee,
        field_name='nationality__name',
        label=_("nationality"),
    )
    area = get_combobox_choices_filter(
        model=Employee,
        field_name='area__name',
        label=_("area"),
    )
    city = get_combobox_choices_filter(
        model=Employee,
        field_name='area__city__name',
        label=_("city"),
    )
    school = get_combobox_choices_filter(
        model=Employee,
        field_name='school',
        label=_("school"),
    )
    specialty = filters.BooleanFilter(
        field_name="is_specialist",
        label=_("specialty"),
        widget=widgets.Select(
            choices=(
                (None, "---------"),
                (True, _("specialist").title()),
                (False, _("supporter").title()),
            )
        ),
    )

    salary_gte, salary_lte = get_decimal_filters("salary")
    local_salary_gte, local_salary_lte = get_decimal_filters("local_salary")
    job_age_gte, job_age_lte = get_number_filters("job_age")
    age_gte, age_lte = get_number_filters("age")
    hire_date_gte, hire_date_lte = get_date_filters("hire_date")

    religion = get_combobox_choices_filter(
        model=Employee,
        field_name='religion',
        label=_("religion"),
        choices=Employee.ReligionChoices.choices,
    )
    martial = get_combobox_choices_filter(
        model=Employee,
        field_name='martial_status',
        label=_("martial"),
        choices=Employee.MartialStatusChoices.choices,
    )
    military = get_combobox_choices_filter(
        model=Employee,
        field_name='military_status',
        label=_("military"),
        choices=Employee.MilitaryStatus.choices,
    )

    class Meta:
        model = Employee
        fields = ["firstname", "gender"]
