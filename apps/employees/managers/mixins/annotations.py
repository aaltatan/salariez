from decimal import Decimal

from django.db import models
from django.db.models import F, ExpressionWrapper, Value, Subquery, OuterRef
from django.db.models.functions import Floor, Coalesce
from django.utils import timezone
from .utils import join_db


class AnnotationsMixin:
    def _annotate_department(
        self, qs: models.QuerySet, contracts: models.QuerySet
    ) -> models.QuerySet:
        """
        Annotates queryset with department information from contracts.

        Args:
            qs: Base employee queryset
            contracts: Contracts queryset containing department info

        Returns:
            Queryset annotated with department_pk and department name
        """
        return qs.annotate(
            department_pk=self.__get_subquery(contracts, "department", "pk"),
            department=self.__get_subquery(
                contracts, "department", "name", default_value="-"
            ),
        )

    def _annotate_cost_center(
        self, qs: models.QuerySet, contracts: models.QuerySet
    ) -> models.QuerySet:
        """
        Annotates queryset with cost center information from contracts.

        Args:
            qs: Base employee queryset
            contracts: Contracts queryset containing cost center info

        Returns:
            Queryset annotated with cost_center_pk, name and accounting_id
        """
        return qs.annotate(
            cost_center_pk=self.__get_subquery(
                contracts, "department", "cost_center", "pk"
            ),
            cost_center=self.__get_subquery(
                contracts, "department", "cost_center", "name", default_value="-"
            ),
            cost_center_accounting_id=self.__get_subquery(
                contracts,
                "department",
                "cost_center",
                "cost_center_accounting_id",
                default_value="-",
            ),
        )

    def _annotate_job(
        self, qs: models.QuerySet, contracts: models.QuerySet
    ) -> models.QuerySet:
        """
        Annotates queryset with job type and subtype information.

        Args:
            qs: Base employee queryset
            contracts: Contracts queryset containing job info

        Returns:
            Queryset annotated with job type and subtype details
        """
        qs = qs.annotate(
            job_type_pk=self.__get_subquery(contracts, "job_subtype", "job_type", "pk"),
            job_type=self.__get_subquery(
                contracts, "job_subtype", "job_type", "name", default_value="-"
            ),
            job_subtype_pk=self.__get_subquery(contracts, "job_subtype", "pk"),
            job_subtype=self.__get_subquery(
                contracts, "job_subtype", "name", default_value="-"
            ),
        )
        return qs

    def _annotate_position(
        self, qs: models.QuerySet, contracts: models.QuerySet
    ) -> models.QuerySet:
        """
        Annotates queryset with employee position information.

        Args:
            qs: Base employee queryset
            contracts: Contracts queryset containing position info

        Returns:
            Queryset annotated with position pk, name and order
        """
        qs = qs.annotate(
            position_pk=self.__get_subquery(contracts, "position", "pk"),
            position=self.__get_subquery(
                contracts, "position", "name", default_value="-"
            ),
            position_order=self.__get_subquery(
                contracts, "position", "order", default_value=1000
            ),
        )
        return qs

    def _annotate_status(
        self, qs: models.QuerySet, contracts: models.QuerySet
    ) -> models.QuerySet:
        """
        Annotates queryset with employee status information.

        Args:
            qs: Base employee queryset
            contracts: Contracts queryset containing status info

        Returns:
            Queryset annotated with status pk and name
        """
        qs = qs.annotate(
            status_pk=self.__get_subquery(contracts, "status", "pk"),
            status=self.__get_subquery(contracts, "status", "name", default_value="-"),
        )
        return qs

    def _annotate_currency(
        self,
        qs: models.QuerySet,
        contracts: models.QuerySet,
        exchange_rates: models.QuerySet,
    ) -> models.QuerySet:
        """
        Annotates queryset with currency and exchange rate information.

        Args:
            qs: Base employee queryset
            contracts: Contracts queryset containing currency info
            exchange_rates: Exchange rates queryset

        Returns:
            Queryset annotated with currency details and exchange rate
        """
        return qs.annotate(
            currency_pk=self.__get_subquery(contracts, "currency", "pk"),
            currency=self.__get_subquery(
                contracts, "currency", "name", default_value="_"
            ),
            currency_short=self.__get_subquery(
                contracts, "currency", "short_name", default_value="_"
            ),
            currency_fraction=self.__get_subquery(
                contracts, "currency", "fraction_name", default_value="_"
            ),
            exchange_rate=self.__get_subquery(
                exchange_rates,
                "rate",
                default_value=1,
                output_field=models.DecimalField(max_digits=20, decimal_places=2),
            ),
        )

    def _annotate_salary(
        self, qs: models.QuerySet, contracts: models.QuerySet
    ) -> models.QuerySet:
        """
        Annotates queryset with salary information including local currency conversion.

        Args:
            qs: Base employee queryset
            contracts: Contracts queryset containing salary info

        Returns:
            Queryset annotated with salary and local_salary (converted using exchange rate)
        """
        return qs.annotate(
            salary=Coalesce(
                Subquery(contracts.values("salary")[:1]), Value(Decimal(0))
            ),
            local_salary=F("exchange_rate") * F("salary"),
        )

    def _annotate_education(
        self, qs: models.QuerySet, education: models.QuerySet
    ) -> models.QuerySet:
        """
        Annotates queryset with employee education information.

        Args:
            qs: Base employee queryset
            education: Education queryset containing academic details

        Returns:
            Queryset annotated with school, specialization, degree and graduation details
        """
        qs = qs.annotate(
            school_pk=self.__get_subquery(education, "school", "pk"),
            school=self.__get_subquery(education, "school", "name", default_value="-"),
            specialization_pk=self.__get_subquery(education, "specialization", "pk"),
            specialization=self.__get_subquery(
                education, "specialization", "name", default_value="-"
            ),
            is_specialist=self.__get_subquery(
                education, "specialization", "is_specialist", default_value=False
            ),
            education_degree_pk=self.__get_subquery(education, "degree", "pk"),
            education_degree=self.__get_subquery(
                education, "degree", "name", default_value="-"
            ),
            education_order=self.__get_subquery(
                education, "degree", "order", default_value=1000
            ),
            is_academic=self.__get_subquery(
                education, "degree", "is_academic", default_value=False
            ),
            graduation_date=self.__get_subquery(education, "graduation_date"),
        )
        return qs

    def _annotate_names(self, qs: models.QuerySet) -> models.QuerySet:
        """
        Annotates queryset with different name formats and search field.

        Args:
            qs: Base employee queryset

        Returns:
            Queryset annotated with full_name, short_name and search field
        """
        return qs.annotate(
            full_name=join_db("firstname", "father_name", "lastname"),
            short_name=join_db("firstname", "lastname"),
            search=join_db("full_name", "national_id", "full_name"),
        )

    def _annotate_ages(self, qs: models.QuerySet) -> models.QuerySet:
        """
        Annotates queryset with age and job tenure calculations.

        Args:
            qs: Base employee queryset

        Returns:
            Queryset annotated with age and job_age (years of service)
        """
        return qs.annotate(
            age=ExpressionWrapper(
                Floor(
                    (timezone.now().date() - F("birth_date"))
                    / timezone.timedelta(days=365)
                ),
                output_field=models.IntegerField(),
            ),
            job_age=ExpressionWrapper(
                Floor(
                    (timezone.now().date() - F("hire_date"))
                    / timezone.timedelta(days=365)
                ),
                output_field=models.IntegerField(),
            ),
        )

    def __get_subquery(
        self,
        manager,
        *args: tuple[str],
        default_value: str | None = None,
        output_field: models.Field | None = None,
    ) -> Coalesce | Subquery:
        """
        Helper method to generate subqueries with optional default values.

        Args:
            manager: Base queryset manager
            *args: Field lookups to join with double underscores
            default_value: Optional default value if subquery returns None
            output_field: Optional output field type for the annotation

        Returns:
            Subquery expression with optional Coalesce wrapper if default_value provided
        """
        args = "__".join(args)

        subquery = Subquery(manager.values(args)[:1])

        if default_value:
            return Coalesce(subquery, Value(default_value), output_field=output_field)

        return subquery

    def _get_contract_manager(self):
        """
        Returns a configured Contract queryset manager with related fields.

        Returns:
            Contract queryset filtered by employee and ordered by start date
        """
        from ...models import Contract

        return (
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

    def _get_education_manager(self):
        """
        Returns a configured Education queryset manager with related fields.

        Returns:
            Education queryset filtered by current records and ordered by order field
        """
        from ...models import EducationTransaction

        return (
            EducationTransaction.objects.filter(
                is_current=True, employee=OuterRef("pk")
            )
            .select_related("employee", "specialization", "degree", "school")
            .order_by("order")
        )

    def _get_exchange_rates_manager(self):
        """
        Returns a configured ExchangeRate queryset manager.

        Returns:
            Exchange rates queryset filtered by currency and ordered by date
        """
        from apps.exchange_rates.models import ExchangeRate

        return ExchangeRate.objects.filter(
            currency__name=OuterRef("currency")
        ).order_by("-date")
