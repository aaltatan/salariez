from decimal import Decimal

from django.db import models
from django.db.models import F, ExpressionWrapper, Value, Subquery
from django.db.models.functions import Floor, Coalesce
from django.utils import timezone

from .utils import join_db
from .helper import ManagerHelperMixin
from ...querysets import EmployeeQuerySet


class QuerySetManagerMixin(ManagerHelperMixin):
     
    def get_queryset(self) -> models.QuerySet:

        qs = EmployeeQuerySet(self.model, using=self._db)

        qs = qs.select_related('area', 'nationality')
        qs = qs.prefetch_related(
            'mobiles', 'phones', 'emails', 'education_transactions', 'groups'
        )

        contracts = self._get_contract_manager()
        education = self._get_education_manager()
        exchange_rates = self._get_exchange_rates_manager()

        qs = qs.annotate(
            department_pk=self._get_subquery(
                 contracts, 'department', 'pk'
            ),
            department=self._get_subquery(
                contracts, "department", "name", default_value='-'
            ),
        )

        qs = qs.annotate(
            cost_center_pk=self._get_subquery(
                 contracts, 'department', 'cost_center', 'pk'
            ),
            cost_center=self._get_subquery(
                 contracts, "department", "cost_center", "name", default_value='-'
            ),
            cost_center_accounting_id=self._get_subquery(
                contracts, 
                "department", 
                "cost_center", 
                "cost_center_accounting_id", 
                default_value='-'
            ),
        )

        qs = qs.annotate(
            job_type_pk=self._get_subquery(
                 contracts, 'job_subtype', 'job_type', 'pk'
            ),
            job_type=self._get_subquery(
                 contracts, "job_subtype", "job_type", "name", default_value='-'
            ),
        )

        qs = qs.annotate(
            job_subtype_pk=self._get_subquery(contracts, 'job_subtype', 'pk'),
            job_subtype=self._get_subquery(
                 contracts, "job_subtype", "name", default_value='-'
            ),
        )

        qs = qs.annotate(
            status_pk=self._get_subquery(contracts, 'status', 'pk'),
            status=self._get_subquery(contracts, "status", "name", default_value="-"),
        )

        qs = qs.annotate(
            position_pk=self._get_subquery(contracts, 'position', 'pk'),
            position=self._get_subquery(contracts, "position", "name", default_value="-"),
            position_order=self._get_subquery(
                 contracts, "position", "order", default_value=1000
            ),
        )

        qs = qs.annotate(
            currency_pk=self._get_subquery(contracts, 'currency', 'pk'),
            currency=self._get_subquery(
                contracts, "currency", "name", default_value="_"
            ),
            currency_short=self._get_subquery(
                contracts, "currency", "short_name", default_value="_"
            ),
            currency_fraction=self._get_subquery(
                contracts, "currency", "fraction_name", default_value="_"
            ),
            exchange_rate=self._get_subquery(
                exchange_rates, 
                'rate', 
                default_value=1, 
                output_field=models.DecimalField(
                    max_digits=20, decimal_places=2
                )
            )
        )

        qs = qs.annotate(
            salary=Coalesce(
                Subquery(contracts.values('salary')[:1]),
                Value(Decimal(0))
            ),
            local_salary=F("exchange_rate") * F("salary"),
        )

        qs = qs.annotate(
            school_pk=self._get_subquery(education, 'school', 'pk'),
            school=self._get_subquery(
                education, "school", "name", default_value='-'
            ),
        )

        qs = qs.annotate(
            specialization_pk=self._get_subquery(
                education, 'specialization', 'pk'
            ),
            specialization=self._get_subquery(
                education, "specialization", "name", default_value='-'
            ),
            is_specialist=self._get_subquery(
                education, "specialization", "is_specialist", default_value=False
            ),
        )

        qs = qs.annotate(
            education_degree_pk=self._get_subquery(
                education, 'degree', 'pk'
            ),
            education_degree=self._get_subquery(
                education, "degree", "name", default_value='-'
            ),
            education_order=self._get_subquery(
                education, "degree", "order", default_value=1000
            ),
            is_academic=self._get_subquery(
                education, "degree", "is_academic", default_value=False
            ),
        )

        qs = qs.annotate(
            graduation_date=self._get_subquery(
                education, 'graduation_date'
            ),
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