from django.forms import widgets
from django.db.models import Model
from django.utils.translation import gettext as _

import django_filters as filters
from django_filters import NumberFilter, CharFilter

from apps.base.utils.fields import get_date_field
from apps.base.widgets import ComboboxWidget


def get_number_filters(field: str) -> tuple[NumberFilter, NumberFilter]:

    gte = filters.NumberFilter(
        field_name=f"{field}__gte",
        method="filter_numbers_and_dates",
        widget=widgets.TextInput({
            "placeholder": _('from'),
        }),
    )

    lte = filters.NumberFilter(
        field_name=f"{field}__lte",
        method="filter_numbers_and_dates",
        widget=widgets.TextInput({
            "placeholder": _('to'),
        }),
    )

    return gte, lte


def get_date_filters(field: str) -> tuple[CharFilter, CharFilter]:

    gte = filters.CharFilter(
        field_name=f"{field}__gte",
        method="filter_numbers_and_dates",
        widget=get_date_field(
            fill_on_focus=False,
            required=False,
            placeholder=_('from')
        )
    )

    lte = filters.CharFilter(
        field_name=f"{field}__lte",
        method="filter_numbers_and_dates",
        widget=get_date_field(
            fill_on_focus=False,
            required=False,
            placeholder=_('to')
        )
    )

    return gte, lte


def get_decimal_filters(field: str) -> tuple[CharFilter, CharFilter]:

    gte = filters.CharFilter(
        field_name=f'{field}__gte',
        method="filter_decimals",
        widget=widgets.TextInput({
            'x-mask:dynamic': '$money($input)',
            'placeholder': _('from'),
        })
    )

    lte = filters.CharFilter(
        field_name=f'{field}__lte',
        method="filter_decimals",
        widget=widgets.TextInput({
            'x-mask:dynamic': '$money($input)',
            'placeholder': _('to'),
        })
    )

    return gte, lte


def get_data_list(model: Model, field_name: str) -> list[tuple]:
    qs = model.objects.values_list(field_name, flat=True)
    return [(f, f) for f in list(set(qs))]


def get_combobox_choices_filter(
    model: Model, 
    field_name: str, 
    label: str,
    method_name: str = 'filter_combobox',
    choices = None
) -> filters.MultipleChoiceFilter:
    
    kwargs = {
        'field_name': field_name,
        'label': label,
        'method': method_name,
        'widget': ComboboxWidget(
            attrs={"data-name": label},
        ),
    }

    if choices is not None:
        kwargs['choices'] = choices
    else:
        kwargs['choices'] = get_data_list(model, field_name)
    
    return filters.MultipleChoiceFilter(**kwargs)