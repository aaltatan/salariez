from decimal import Decimal

from django.db import models
from django.db.models import (
    Value, F, ExpressionWrapper, Count, Subquery, OuterRef
)
from django.db.models.functions import Coalesce, Floor
from django.utils import timezone

from .utils import join_db


class EmployeeQuerySet(models.QuerySet):

    def today_birthdays(self):
        return self.filter(
            birth_date__day=timezone.now().day,
            birth_date__month=timezone.now().month,
        )
    
    def this_month_birthdays(self, upcoming_only: bool = True):
        
        filters = {
            'birth_date__month': timezone.now().month,
        }

        if upcoming_only:
            filters['birth_date__day__gt'] = timezone.now().day
            
        return self.filter(**filters)


class EmployeeManager(models.Manager):

    def get_counts_grouped_by(self, group_by: str = 'gender'):
        return self.get_queryset().values(group_by).annotate(
            counts=Count('pk')
        )

    def get_queryset(self) -> models.QuerySet:

        qs = EmployeeQuerySet(self.model, using=self._db)

        qs = qs.select_related('area', 'nationality')
        qs = qs.prefetch_related(
            'mobiles', 'phones', 'emails', 'education_transactions', 'groups'
        )

        from ..models import EducationTransaction, Contract
        from apps.exchange_rates.models import ExchangeRate

        contracts = (
            Contract.objects.select_related(
                "employee",
                "department",
                "job_subtype",
                "status",
                "position",
                "currency",
            )
            .filter(employee=OuterRef("pk"))
            .order_by("-start_date")
        )

        education = (
            EducationTransaction.objects.filter(
                is_current=True, employee=OuterRef("pk")
            )
            .select_related("employee", "specialization", "degree", "school")
            .order_by("order")
        )

        def get_subquery_contract(
            *args: tuple[str], value: str = "-"
        ) -> Coalesce:
            args = "__".join(args)

            return Coalesce(
                Subquery(contracts.values(args)[:1]), Value(value)
            )

        def get_subquery_education(
            *args: tuple[str], value: str = "-"
        ) -> Coalesce:
            args = "__".join(args)

            return Coalesce(
                Subquery(education.values(args)[:1]), Value(value)
            )

        qs = qs.annotate(
            department_pk=Subquery(
                contracts.values("department__pk")[:1]
            ),
            department=get_subquery_contract("department", "name"),
        )

        qs = qs.annotate(
            cost_center_pk=Subquery(
                contracts.values("department__cost_center__pk")[:1]
            ),
            cost_center=get_subquery_contract("department", "cost_center", "name"),
            cost_center_accounting_id=get_subquery_contract(
                "department", "cost_center", "cost_center_accounting_id"
            ),
        )

        qs = qs.annotate(
            job_type_pk=Subquery(contracts.values("job_subtype__job_type__pk")[:1]),
            job_type=get_subquery_contract("job_subtype", "job_type", "name"),
        )

        qs = qs.annotate(
            job_subtype_pk=Subquery(contracts.values("job_subtype__pk")[:1]),
            job_subtype=get_subquery_contract("job_subtype", "name"),
        )

        qs = qs.annotate(
            status_pk=Subquery(contracts.values("status__pk")[:1]),
            status=get_subquery_contract("status", "name"),
        )

        qs = qs.annotate(
            position_pk=Subquery(contracts.values("position__pk")[:1]),
            position=get_subquery_contract("position", "name"),
            position_order=get_subquery_contract("position", "order", value=1000),
        )

        qs = qs.annotate(
            currency_pk=Subquery(contracts.values("currency__pk")[:1]),
            currency=get_subquery_contract("currency", "name"),
            currency_short=get_subquery_contract("currency", "short_name"),
            currency_fraction=get_subquery_contract("currency", "fraction_name"),
            exchange_rate=Coalesce(
                Subquery(
                    ExchangeRate.objects.filter(currency__name=OuterRef("currency"))
                    .order_by("-date")
                    .values("rate")[:1]
                ),
                Value(Decimal(1)),
                output_field=models.DecimalField(max_digits=20, decimal_places=2),
            ),
        )

        qs = qs.annotate(
            salary=get_subquery_contract("salary", value=Decimal(0)),
            local_salary=F("exchange_rate") * F("salary"),
        )

        qs = qs.annotate(
            school_pk=Subquery(education.values("school__pk")[:1]),
            school=get_subquery_education("school", "name"),
        )

        qs = qs.annotate(
            specialization_pk=Subquery(education.values("specialization__pk")[:1]),
            specialization=get_subquery_education("specialization", "name"),
            is_specialist=get_subquery_education(
                "specialization", "is_specialist", value=False
            ),
        )

        qs = qs.annotate(
            education_degree_pk=Subquery(education.values("degree__pk")[:1]),
            education_degree=get_subquery_education("degree", "name"),
            education_order=get_subquery_education("degree", "order", value=1000),
            is_academic=get_subquery_education("degree", "is_academic", value=False),
        )

        qs = qs.annotate(
            graduation_date=Subquery(education.values("graduation_date")[:1]),
        )

        qs = qs.annotate(
            full_name=join_db('firstname', 'father_name', 'lastname'),
            short_name=join_db('firstname', 'lastname'),
            search=join_db('full_name', 'national_id', 'full_name'),
        )

        qs = qs.annotate(
            age=ExpressionWrapper(
                Floor(
                    (timezone.now().date() - F("birth_date")) / 
                    timezone.timedelta(days=365)
                ),
                output_field=models.IntegerField(),
            ),
            job_age=ExpressionWrapper(
                Floor(
                    (timezone.now().date() - F("hire_date")) / 
                    timezone.timedelta(days=365)
                ),
                output_field=models.IntegerField(),
            ),
        )

        return qs