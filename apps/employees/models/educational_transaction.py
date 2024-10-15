from django.db import models
from django.utils.translation import gettext as _

from ..models import Employee

from apps.educational_degrees.models import EducationalDegree
from apps.specializations.models import Specialization
from apps.schools.models import School


class EducationTransaction(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name=_('employee'),
        related_name='education_transactions',
    )
    degree = models.ForeignKey(
        EducationalDegree,
        on_delete=models.PROTECT,
        verbose_name=_('education degree'),
        related_name='education_transactions',
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.PROTECT,
        verbose_name=_('specialization'),
        related_name='education_transactions',
        null=True,
        blank=True,
    )
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        verbose_name=_('school'),
        related_name='education_transactions',
        null=True,
        blank=True,
    )
    graduation_date = models.DateField(
        verbose_name=_('graduation_date'),
        null=True,
        blank=True,
    )
    order = models.IntegerField(
        verbose_name=_('order'),
        help_text=_('order of position'),
        default=1,
    )
    is_current = models.BooleanField(
        verbose_name=_('is current'),
        default=True,
        help_text=_('is it current?'),
    )
    notes = models.TextField(
        verbose_name=_('notes'),
        max_length=1000,
        default='',
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.employee.fullname} {self.degree.name} in {self.specialization}'
    
    def save(self, *args, **kwargs) -> None:
        
        if self.is_current:
            Klass = self.__class__
            qs = Klass.objects.filter(employee=self.employee).all()
            for obj in qs:
                obj.is_current = False
                obj.save()

        return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['employee__firstname', 'order']
        unique_together = [
            ('employee', 'order')
        ]
        permissions = [
            ['can_export', 'Can export data']
        ]