from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _


four_chars_validator = MinLengthValidator(
    4, _('name of the faculty should not be less than 4 characters.')
)

numeric_validator = RegexValidator(
    r'^\d+$', _('department id must be numbers only')
)