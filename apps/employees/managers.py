from typing import Literal
from decimal import Decimal

from django.db import models
from django.db.models import (
    Case, When, Q, Value, F, ExpressionWrapper, Count, Subquery, OuterRef
)
from django.db.models.functions import (
    ExtractYear,
    ExtractMonth,
    ExtractDay,
    TruncDate,
    Coalesce,
    Concat,
    Round,
    Now,
)


LOOKUPS = Literal["", "gt", "gte", "lt", "lte"]


def get_age_timedelta(field_name: str) -> ExpressionWrapper:
    """
    utility function return ExpressionWrapper
    to generate differences between field date and now as database field `MySQL`
    """
    return ExpressionWrapper(
        TruncDate(Now()) - F(field_name), 
        models.DecimalField()
    )


def get_age(field_name: str) -> ExpressionWrapper:
    """
    utility function return ExpressionWrapper
    to calculate age Field in years `MySQL` based on age_timedelta
    """
    return ExpressionWrapper(
        F(field_name) / Value(86_400_000_000) / Value(365),
        models.IntegerField(),
    )


class EmployeeManager(models.Manager):
    
    def get_ages(
        self,
        age: int,
        lookup: LOOKUPS = "",
    ) -> models.QuerySet:
        key = f"age__{lookup}" if lookup else "age"
        return self.get_queryset().filter(**{key: age})

    def get_today_birthdays(self) -> models.QuerySet:
        return self.get_queryset().filter(is_today_birthday=True)
    
    def get_male_female_count(self) -> dict:
        return self.get_queryset().aggregate(
            count=Count('gender'),
            male=Count('gender', filter=Q(gender='m')),
            female=Count('gender', filter=Q(gender='f')),
            male_avg=ExpressionWrapper(
                Round(
                    F('male') / F('count') * Value(100),
                    precision=2
                ), 
                output_field=models.FloatField()
            ),
            female_avg=ExpressionWrapper(
                Round(
                    F('female') / F('count') * Value(100),
                    precision=2
                ), 
                output_field=models.FloatField()
            ),
        )

    def get_upcoming_birthdays_this_month(self) -> models.QuerySet:
        return self.get_queryset().filter(is_month_birthday=True)

    def get_upcoming_job_anniversaries_this_month(
        self,
        oldness_years: int = 1,
        taking_pasts: bool = False,
        lookup: LOOKUPS = "",
    ) -> models.QuerySet:
        if oldness_years <= 0:
            raise ValueError(
                "oldness_years must be grater than or equal than 1"
            )

        key = "oldness_years_taking_pasts" if taking_pasts else "oldness_years"

        if lookup:
            key = f"{key}__{lookup}"

        return self.get_queryset().filter(**{key: oldness_years})

    def get_today_job_anniversaries(self) -> models.QuerySet:
        return self.get_queryset().filter(is_today_job_anniversary=True)

    def get_queryset(self) -> models.QuerySet:

        from .models import EducationTransaction, Contract
        from apps.exchange_rates.models import ExchangeRate

        contracts = (
            Contract
            .objects
            .select_related(
                "employee", "department", "job_subtype", 
                "status", "position", "currency"
            )
            .filter(employee=OuterRef('pk'))
            .order_by("-start_date")
        )

        education = (
            EducationTransaction
            .objects
            .filter(is_current=True, employee=OuterRef("pk"))
            .select_related(
                "employee", "specialization", "degree", "school"
            )
            .order_by("order")
        )

        return (
            super()
            .get_queryset()
            .annotate(
                # ------ contract information ------#
                department=Coalesce(
                    Subquery(
                        contracts.values('department__name')[:1]
                    ), Value('-')
                ),
                # department_pk=Coalesce(
                #     Subquery(
                #         contracts.values('department__pk')[:1]
                #     ), Value('-')
                # ),
                cost_center=Coalesce(
                    Subquery(
                        contracts.values('department__cost_center__name')[:1]
                    ), Value('-')
                ),
                # cost_center_pk=Coalesce(
                #     Subquery(
                #         contracts.values('department__cost_center__pk')[:1]
                #     ), Value('-')
                # ),
                job_type=Coalesce(
                    Subquery(
                        contracts.values('job_subtype__job_type__name')[:1]
                    ), Value('-')
                ),
                # job_type_pk=Coalesce(
                #     Subquery(
                #         contracts.values('job_subtype__job_type__pk')[:1]
                #     ), Value('-')
                # ),
                job_subtype=Coalesce(
                    Subquery(
                        contracts.values('job_subtype__name')[:1]
                    ), Value('-')
                ),
                # job_subtype_pk=Coalesce(
                #     Subquery(
                #         contracts.values('job_subtype__pk')[:1]
                #     ), Value('-')
                # ),
                status=Coalesce(
                    Subquery(
                        contracts.values('status__name')[:1]
                    ), Value('-')
                ),
                # status_pk=Coalesce(
                #     Subquery(
                #         contracts.values('status__pk')[:1]
                #     ), Value('-')
                # ),
                position=Coalesce(
                    Subquery(
                        contracts.values('position__name')[:1]
                    ), Value('-')
                ),
                # position_pk=Coalesce(
                #     Subquery(
                #         contracts.values('position__pk')[:1]
                #     ), Value('-')
                # ),
                salary=Coalesce(
                    Subquery(
                        contracts.values('salary')[:1]
                    ), Value(Decimal(0))
                ),
                currency=Coalesce(
                    Subquery(
                        contracts.values('currency__name')[:1]
                    ), Value('-')
                ),
                # currency_pk=Coalesce(
                #     Subquery(
                #         contracts.values('currency__pk')[:1]
                #     ), Value('-')
                # ),
                currency_short=Coalesce(
                    Subquery(
                        contracts.values('currency__short_name')[:1]
                    ), Value('-')
                ),
                currency_fraction=Coalesce(
                    Subquery(
                        contracts.values('currency__fraction_name')[:1]
                    ), Value('-')
                ),
                exchange_rate=Coalesce(
                    Subquery(
                        ExchangeRate.objects.filter(
                            currency__name=OuterRef('currency')
                        ).order_by('-date').values('rate')[:1]
                    ),
                    Value(Decimal(1)),
                    output_field=models.DecimalField(
                        max_digits=20, decimal_places=2
                    )
                ),
                local_salary=F('exchange_rate') * F('salary'),
                # ------ education information ------#
                school=Coalesce(
                    Subquery(
                        education.values('school__name')[:1]
                    ), Value('-')
                ),
                # school_pk=Coalesce(
                #     Subquery(
                #         education.values('school__pk')[:1]
                #     ), Value('-')
                # ),
                specialization=Coalesce(
                    Subquery(
                        education.values('specialization__name')[:1]
                    ), Value('-')
                ),
                # specialization_pk=Coalesce(
                #     Subquery(
                #         education.values('specialization__pk')[:1]
                #     ), Value('-')
                # ),
                education_degree=Coalesce(
                    Subquery(
                        education.values('degree__name')[:1]
                    ), Value('-')
                ),
                # education_degree_pk=Coalesce(
                #     Subquery(
                #         education.values('degree__pk')[:1]
                #     ), Value('-')
                # ),
                education_order=Coalesce(
                    Subquery(
                        education.values('degree__order')[:1]
                    ), Value(1000)
                ),
                is_academic=Coalesce(
                    Subquery(
                        education.values('degree__is_academic')[:1]
                    ), False
                ),
                is_specialist=Coalesce(
                    Subquery(
                        education
                        .values('specialization__is_specialist')[:1]
                    ), False
                ),
                graduation_date=Subquery(
                    education.values('graduation_date')[:1]
                ),
                # ------ start helpers ------#
                birth_year=ExtractYear("birth_date"),
                birth_month=ExtractMonth("birth_date"),
                birth_day=ExtractDay("birth_date"),
                hire_year=ExtractYear("hire_date"),
                hire_month=ExtractMonth("hire_date"),
                hire_day=ExtractDay("hire_date"),
                # ------- end helpers -------#
                # calculating the ages (not precisely)
                job_age_timedelta=get_age_timedelta("hire_date"),
                job_age=get_age("job_age_timedelta"),
                age_timedelta=get_age_timedelta("birth_date"),
                age=get_age("age_timedelta"),
                # ---------------------------#
                full_name=Concat(
                    models.F("firstname"),
                    models.Value(" "),
                    models.F("father_name"),
                    models.Value(" "),
                    models.F("lastname"),
                ),
                short_name=Concat(
                    models.F("firstname"),
                    models.Value(" "),
                    models.F("lastname"),
                ),
                search=Concat(
                    models.F("full_name"),
                    models.Value(" "),
                    models.F("full_name"),
                ),
                # -------- birthdays --------#
                # calculating if the current month is the birthday month
                # if it is, it's return True taking if the has finished or not.
                is_month_birthday=Case(
                    When(
                        Q(birth_month=ExtractMonth(Now()))
                        & Q(birth_day__gte=ExtractDay(Now())),
                        then=True,
                    ),
                    default=False,
                    output_field=models.BooleanField(),
                ),
                is_today_birthday=Case(
                    When(
                        Q(birth_month=ExtractMonth(Now()))
                        & Q(birth_day=ExtractDay(Now())),
                        then=True,
                    ),
                    default=False,
                    output_field=models.BooleanField(),
                ),
                # ----- job_anniversaries ---#
                oldness_years=Case(
                    When(
                        condition=Q(hire_month=ExtractMonth(Now())),
                        then=ExpressionWrapper(
                            ExtractYear(Now()) - F("hire_year"),
                            output_field=models.IntegerField(),
                        ),
                    ),
                    default=0,
                    output_field=models.IntegerField(),
                ),
                is_today_job_anniversary=Case(
                    When(
                        Q(hire_month=ExtractMonth(Now()))
                        & Q(hire_day=ExtractDay(Now())),
                        then=True,
                    ),
                    default=False,
                    output_field=models.BooleanField(),
                ),
                oldness_years_taking_pasts=Case(
                    When(
                        Q(hire_month=ExtractMonth(Now()))
                        & Q(hire_day__gte=ExtractDay(Now())),
                        then=ExpressionWrapper(
                            ExtractYear(Now()) - F("hire_year"),
                            output_field=models.IntegerField(),
                        ),
                    ),
                    default=0,
                    output_field=models.IntegerField(),
                ),
            )
        )
