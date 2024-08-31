from django import template


register = template.Library()


@register.filter
def multiply(value: str, arg: int):
    value = int(value)
    arg = int(arg)
    return arg * value