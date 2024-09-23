from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import EmployeeManager

from apps.base.validators import (
    two_chars_validator,
    numeric_validator,
)
from apps.nationalities.models import Nationality
from apps.areas.models import Area
from apps.departments.models import Department
from apps.job_subtypes.models import JobSubtype
from apps.positions.models import Position
from apps.statuses.models import Status


class Employee(models.Model):
    
    class StatusChoices(models.TextChoices):
        ACTIVE = 'A', _('active').title()
        INACTIVE = 'I', _('inactive').title()
    
    class GenderChoices(models.TextChoices):
        MALE = 'M', _('male').title()
        FEMALE = 'F', _('female').title()
    
    class MartialStatusChoices(models.TextChoices):
        MARRIED = 'M', _('married').title()
        SINGLE = 'S', _('single').title()
        DIVORCED = 'D', _('divorced').title()
        OTHER = 'O', _('other').title()
    
    class MilitaryStatus(models.TextChoices):
        DEFREMENTED = 'D', _('defremented').title()
        FINISHED = 'F', _('finished').title()
        EXCUSED = 'E', _('excused').title()
        OTHER = 'O', _('other').title()

    objects = EmployeeManager()

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='employees'
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='employees'
    )
    firstname = models.CharField(
        max_length=255,
        verbose_name=_('first name'),
        validators=[two_chars_validator]
    )
    lastname = models.CharField(
        max_length=255,
        verbose_name=_('last name'),
        validators=[two_chars_validator]
    )
    father_name = models.CharField(
        max_length=255,
        verbose_name=_('father name'),
        validators=[two_chars_validator]
    )
    mother_name = models.CharField(
        max_length=255,
        verbose_name=_('mother name'),
        validators=[two_chars_validator]
    )
    birth_place = models.CharField(
        max_length=255,
        verbose_name=_('birth place'),
        validators=[two_chars_validator]
    )
    birth_date = models.DateField()
    national_id = models.CharField(
        max_length=255,
        verbose_name=_('national id'),
        unique=True,
        validators=[numeric_validator]
    )
    card_id = models.CharField(
        max_length=255,
        verbose_name=_('card id'),
        unique=True,
        null=True,
        validators=[numeric_validator]
    )
    # أمانة السجل المدني
    civil_registry_office = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name=_('civil registry office'),
    )
    # قيد السجل المدني
    registry_office_name = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name=_('registry office name'),
    )
    # رقم السجل المدني
    registry_office_id = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name=_('registry office id'),
        validators=[numeric_validator]
    )
    gender = models.CharField(
        max_length=6,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE,
    )
    face_color = models.CharField(
        max_length=255, default='', blank=True, verbose_name=_('face color')
    )
    eyes_color = models.CharField(
        max_length=255, default='', blank=True, verbose_name=_('eyes color')
    )
    address = models.CharField(
        max_length=255, default='', blank=True, verbose_name=_('address')
    )
    special_signs = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name=_('special signs'),
    )
    card_date = models.DateField(null=True, blank=True)
    martial_status = models.CharField(
        max_length=6,
        choices=MartialStatusChoices.choices,
        default=MartialStatusChoices.SINGLE,
    )
    military_status = models.CharField(
        max_length=6,
        choices=MilitaryStatus.choices,
        default=MilitaryStatus.EXCUSED,
    )
    nationality = models.ForeignKey(
        Nationality, on_delete=models.PROTECT, related_name='employees'
    )
    area = models.ForeignKey(
        Area, on_delete=models.PROTECT, related_name='employees'
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='employees'
    )
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name='employees'
    )
    job_subtype = models.ForeignKey(
        JobSubtype, on_delete=models.PROTECT, related_name='employees'
    )
    job_status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name='employees'
    )
    status = models.CharField(
        max_length=7,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )
    activate_date = models.DateField(blank=True, null=True)
    deactivate_date = models.DateField(blank=True, null=True)
    hire_date = models.DateField()
    institution_id = models.CharField(
        max_length=255,
        verbose_name=_('institution id'),
        unique=True,
        null=True,
        validators=[numeric_validator]
    )
    notes = models.TextField(
        verbose_name=_('notes'),
        max_length=1000,
        default='',
        blank=True
    )
    profile = models.ImageField(
        upload_to='profiles', null=True, blank=True
    )
    identity_document = models.FileField(
        upload_to='identities', null=True, blank=True
    )
    salary = models.DecimalField(
        decimal_places=2, max_digits=12, default=0,
    )

    def save(self, *args, **kwargs) -> None:
        
        if self.activate_date is None:
            self.activate_date = timezone.now().date()
        
        if self.gender == self.GenderChoices.FEMALE.value:
            self.military_status = self.MilitaryStatus.EXCUSED.value

        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.firstname} {self.father_name} {self.lastname}'