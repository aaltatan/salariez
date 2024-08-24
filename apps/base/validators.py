from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


four_chars = MinLengthValidator(
    4, _('name of the faculty should not be less than 4 characters.')
)
