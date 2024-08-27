import re

from django.utils.text import slugify
from django.db import models


def increase_last_digit(string: str) -> str:
    """
    increase last digit in given string by one  
    e.g.: google-1 -> google-2  
    e.g.: google -> google-1
    """
    regex = re.compile(r'.+\-\d+')
    digit_regex = re.compile(r'\d+')
    
    if regex.search(string):
        digit = digit_regex.findall(string)[0]
        digit = str(int(digit) + 1)
        string = digit_regex.sub(digit, string)
    else:
        string = f'{string}-1'
        
    return string


def dict_to_css(styles: dict[str, str]) -> str:
    """
    turn a python dict into css string  
    e.g.: {'background': 'red', 'opacity': 0.5} -> 
            'background: red; opacity: 0.5'
    """
    styles = [f'{k}: {v}' for k, v in styles.items()]
    return '; '.join(styles) + ';'


def parse_decimals(numeric: str | None) -> int | float:
    """
    parse string decimal into integer or float number  
    e.g.: '12,000.00' -> 12000  
    e.g.: '12,000.12' -> 12000.12
    """
    if numeric is None or numeric == '':
        return 0
    
    regex = re.compile(r'[^\d\.,]', re.DOTALL)
    numeric = regex.sub('', numeric)
    
    if '.' in numeric:
        number, decimals, *_ = numeric.split('.', 2)
        number = number.replace(',', '')
        
        if ',' in decimals:
            decimals = decimals.split(',')[0]
            
        return float(f'{number}.{decimals}')
    
    numeric = numeric.replace(',', '')
    return int(numeric)


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