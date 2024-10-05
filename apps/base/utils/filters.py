from django.forms import widgets
from django.utils.translation import gettext as _

import django_filters as filters
from django_filters import NumberFilter, CharFilter

from apps.base.utils.fields import get_date_field


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