from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator

from .employee import Employee


phone_validator = RegexValidator(
    r'^0\d{2}\d{4,8}$',
    'phone number must be like 0332756651'
)


class Phone(models.Model):

    employee = models.ForeignKey(
      Employee, on_delete=models.CASCADE, related_name='phones'
    )
    phone = models.CharField(
        max_length=255, 
        verbose_name=_('phone'),
        help_text=_('phone number must be like 0332756651'),
        validators=[phone_validator]
    )
    notes = models.CharField(
        max_length=255, default='', blank=True
    )

    @property
    def get_absolute_path(self) -> str:
        return f'tel:+963{self.phone[1:]}'

    def __str__(self) -> str:
        return f'{self.employee.fullname} [{self.phone}]]'
    
    class Meta:
        unique_together = [
            ['employee', 'phone']
        ]