from decimal import Decimal

from django import template


register = template.Library()


@register.filter
def money(value: int | float | Decimal):
    return f'{float(value):2,}'