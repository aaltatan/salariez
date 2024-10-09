from django import template



register = template.Library()


@register.filter
def ancestors(object) -> bool:
    return object.department.get_ancestors(include_self=True)