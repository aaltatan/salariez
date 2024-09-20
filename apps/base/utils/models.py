from django.utils.text import slugify
from django.db import models

from .text import increase_last_digit


def slugify_instance(
    instance, 
    field: str = 'name', 
    new_slug: str | None = None
):
    """
    add slug property to the instance by chosen field
    """
    if new_slug is None:
        if instance.slug is None:
            field = getattr(instance, field)
            slug = slugify(field, allow_unicode=True)
        else:
            slug = instance.slug
    else:
        slug = new_slug
        
    Klass: models.Model = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    
    if qs.exists():
        slug = increase_last_digit(slug)
        return slugify_instance(instance, field, new_slug=slug)

    instance.slug = slug
    
    return instance