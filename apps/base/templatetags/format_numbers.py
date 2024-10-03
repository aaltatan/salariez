from django import template


register = template.Library()


@register.filter
def money(value: int | float):
    return f'{value:2,}'