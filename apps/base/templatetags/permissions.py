from django import template
from django.contrib.auth.models import User


register = template.Library()


@register.filter
def has_perm(user: User, permission) -> bool:
    return user.has_perm(permission)