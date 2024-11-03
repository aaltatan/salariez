from django.db import models

from .mixins.annotations import AnnotationsMixin
from .mixins.optimizations import OptimizationsMixin
from .mixins.aggregations import AggregationsMixin
from .querysets import EmployeeQuerySet


class EmployeeManager(
    OptimizationsMixin, 
    AnnotationsMixin, 
    AggregationsMixin,
    models.Manager,
):

    def get_queryset(self) -> models.QuerySet:
        
        qs = EmployeeQuerySet(self.model, using=self._db)

        qs = self._select_related(qs)
        qs = self._prefetch_related(qs)

        contracts = self._get_contract_manager()
        education = self._get_education_manager()
        exchange_rates = self._get_exchange_rates_manager()

        qs = self._annotate_department(qs, contracts)
        qs = self._annotate_cost_center(qs, contracts)
        qs = self._annotate_job(qs, contracts)
        qs = self._annotate_position(qs, contracts)
        qs = self._annotate_status(qs, contracts)
        qs = self._annotate_currency(qs, contracts, exchange_rates)
        qs = self._annotate_salary(qs, contracts)
        qs = self._annotate_education(qs, education)
        qs = self._annotate_names(qs)
        qs = self._annotate_ages(qs)

        return qs