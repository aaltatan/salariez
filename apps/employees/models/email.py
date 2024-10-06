from django.db import models
from django.utils.translation import gettext as _

from .employee import Employee


class Email(models.Model):

    employee = models.ForeignKey(
      Employee, on_delete=models.CASCADE, related_name='emails'
    )
    email = models.EmailField(
        max_length=255, verbose_name=_('email'), unique=True
    )
    notes = models.CharField(
        max_length=255, default='', blank=True
    )

    @property
    def get_absolute_path(self) -> str:
        return f'mailto:{self.email}'
    
    def __str__(self) -> str:
        return f'{self.employee.fullname} [{self.email}]]'