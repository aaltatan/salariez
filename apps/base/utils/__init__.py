from .fields import get_search_field, Object
from .models import slugify_instance
from .generic import dict_to_css, parse_decimals, increase_last_digit
from .views import Deleter


__all__ = [
    get_search_field,
    slugify_instance,
    dict_to_css,
    parse_decimals,
    increase_last_digit,
    Object,
    Deleter,
]
