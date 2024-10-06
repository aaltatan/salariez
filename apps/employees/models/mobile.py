from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator

from .employee import Employee


mobile_validator = RegexValidator(
    r'^09\d{8}$',
    'mobile number must be like 0947302503'
)


class Mobile(models.Model):

    employee = models.ForeignKey(
      Employee, on_delete=models.CASCADE, related_name='mobiles'
    )
    mobile = models.CharField(
        max_length=255, 
        verbose_name=_('mobile'),
        unique=True,
        help_text=_('mobile number must be like 0947302503'),
        validators=[mobile_validator]
    )
    has_whatsapp = models.BooleanField(default=True)
    notes = models.CharField(
        max_length=255, default='', blank=True
    )

    @property
    def get_absolute_path(self) -> str:
        return f'tel:+963{self.mobile[1:]}'

    def __str__(self) -> str:
        return f'{self.employee.fullname} [{self.mobile}]]'