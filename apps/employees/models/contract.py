from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_init, pre_save

from .employee import Employee

from apps.departments.models import Department
from apps.job_subtypes.models import JobSubtype
from apps.statuses.models import Status
from apps.positions.models import Position
from apps.currencies.models import Currency

from apps.base.validators import numeric_validator


class Contract(models.Model):
    
    class ContractTypeChoices(models.TextChoices):
        FULLTIME = 'F', _('fulltime').title()
        PARTTIME = 'P', _('parttime').title()

    class OwnershipChoices(models.TextChoices):
        OWNED = 'O', _('owned').title()
        LOANED = 'L', _('loaned').title()

    employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name='contracts',
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='contracts',
    )
    job_subtype = models.ForeignKey(
        JobSubtype, on_delete=models.PROTECT, related_name='contracts',
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name='contracts',
    )
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name='contracts',
    )
    contract_type = models.CharField(
        max_length=10,
        choices=ContractTypeChoices.choices,
        default=ContractTypeChoices.FULLTIME,
    )
    ownership = models.CharField(
        max_length=10,
        choices=OwnershipChoices.choices,
        default=OwnershipChoices.OWNED,
    )
    salary = models.DecimalField(
        decimal_places=2, max_digits=12, default=0
    )
    local_salary = models.DecimalField(
        decimal_places=2, max_digits=12, default=0
    )
    currency = models.ForeignKey(
        Currency, 
        related_name='contracts', 
        on_delete=models.PROTECT,
        default=Currency.get_default_pk
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    institution_id = models.CharField(
        max_length=255,
        verbose_name=_('institution id'),
        unique=True,
        null=True,
        blank=True,
        validators=[numeric_validator]
    )
    notes = models.TextField(
        verbose_name=_('notes'),
        max_length=1000,
        default='',
        blank=True
    )

    @property
    def has_salary(self) -> bool:
        
        if getattr(self, 'status', None) is None:
            return False

        if self.status.has_salary is False:
            return False

        if self.end_date is not None:
            today = timezone.datetime.today().date()
            if self.end_date < today:
                return False
        
        return True

    def clean(self) -> None:

        start_date = self.start_date
        end_date = self.end_date

        if end_date is not None and end_date < start_date:
            raise ValidationError(
                _('end date must be greater than start date')
            )

        qs = self.__class__.objects.filter(
            employee=self.employee,
            start_date__gte=start_date, 
        )

        if self.pk is not None:
            qs = self.__class__.objects.filter(
                employee=self.employee,
                start_date__gte=start_date, 
                pk__lt=self.pk
            ).exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError(
                _('the new start date must be greater than the previous ones')
            )
        
        if self.pk is not None:
            qs = self.__class__.objects.filter(
                employee=self.employee, 
                start_date__lte=start_date,
                pk__gt=self.pk
            )
            if qs.exists():
                raise ValidationError(
                    _('the new start date must be less than the next ones')
                )

    def __str__(self) -> str:
        return (
          f'{self.employee.fullname} - {self.position.name} in {self.department.name}'
        )


def calculate_local_price(instance: Contract):
    
    rate = (
        instance
        .currency
        .rates
        .filter(date__lte=timezone.datetime.today().date())
        .order_by('date')
        .last()
        .rate
    )
    instance.local_salary = instance.salary * rate

    if not instance.has_salary:
        instance.local_salary = 0
        instance.salary = 0


def contract_post_init(sender, instance: Contract, *args, **kwargs):
    calculate_local_price(instance)

def contract_pre_save(sender, instance: Contract, *args, **kwargs):
    calculate_local_price(instance)

post_init.connect(contract_post_init, Contract)
pre_save.connect(contract_pre_save, Contract)