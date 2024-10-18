from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, pre_delete
from django.utils.text import slugify

from apps.base.validators import (
    two_chars_validator,
    numeric_validator,
)
from apps.nationalities.models import Nationality
from apps.areas.models import Area


class Employee(models.Model):

    class ReligionChoices(models.TextChoices):
        MUSLIM = 'M', _('muslim').title()
        CHRISTIAN = 'C', _('christian').title()
        JEWISH = 'J', _('jewish').title()
        OTHER = 'O', _('other').title()
    
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
    religion = models.CharField(
        max_length=6,
        choices=ReligionChoices.choices,
        default=ReligionChoices.MUSLIM,
    )
    current_address = models.CharField(
        max_length=255, default='', blank=True
    )
    nationality = models.ForeignKey(
        Nationality, on_delete=models.PROTECT, related_name='employees'
    )
    area = models.ForeignKey(
        Area, on_delete=models.PROTECT, related_name='employees'
    )
    hire_date = models.DateField()
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
    slug = models.SlugField(
        unique=True,
        max_length=255,
        null=True,
        blank=True,
        allow_unicode=True,
    )

    @property
    def fullname(self) -> str:
        return f'{self.firstname} {self.father_name} {self.lastname}'

    @property
    def shortname(self) -> str:
        return f'{self.firstname} {self.lastname}'

    def _get_app_label(self):
        return self.__class__._meta.app_label

    @property
    def get_activity_path(self):
        kwargs = {
            'app_label': self._get_app_label(),
            'model_name': self.__class__.__name__,
            'object_id': self.id,
        }
        return reverse('activities:index', kwargs=kwargs)

    @property
    def get_absolute_path(self):
        return reverse(
            f'{self._get_app_label()}:details',  kwargs={'slug': self.slug}
        )

    @property
    def get_create_path(self):
        return reverse(f'{self._get_app_label()}:create')

    @property
    def get_update_path(self):
        return reverse(
            f'{self._get_app_label()}:update', kwargs={'slug': self.slug}
        )
    
    @property
    def get_delete_path(self):
        return reverse(
            f'{self._get_app_label()}:delete', kwargs={'slug': self.slug}
        )
    
    @property
    def get_contextmenu_path(self):
        return reverse(
            f'{self._get_app_label()}:index', kwargs={'id': self.pk}
        )
    
    def __str__(self) -> str:
        return self.fullname

    class Meta:
        ordering = ['firstname']


def employee_pre_save(sender, instance: Employee, *args, **kwargs):
    instance.slug = slugify(
        f'{instance.fullname}-{instance.national_id}',
        allow_unicode=True
    )
    if instance.gender == instance.GenderChoices.FEMALE.value:
        instance.military_status = instance.MilitaryStatus.EXCUSED.value

def employee_post_delete(sender, instance: Employee, *args, **kwargs):
    instance.profile.delete()


pre_save.connect(employee_pre_save, Employee)
pre_delete.connect(employee_post_delete, Employee)