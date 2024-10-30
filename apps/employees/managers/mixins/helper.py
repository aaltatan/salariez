from django.db import models
from django.db.models import Value, Subquery, OuterRef
from django.db.models.functions import Coalesce


class ManagerHelperMixin:

    def _get_subquery(
            self,
            manager, 
            *args: tuple[str], 
            default_value: str | None = None,
            output_field: models.Field | None = None
        ) -> Coalesce | Subquery:
            
            args = "__".join(args)

            subquery = Subquery(manager.values(args)[:1])

            if default_value:
                return Coalesce(subquery, Value(default_value), output_field=output_field)
            
            return subquery
    
    def _get_contract_manager(self):
        
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

        from ...models import EducationTransaction
        
        return (
            EducationTransaction
            .objects
            .filter(
                is_current=True, employee=OuterRef("pk")
            )
            .select_related(
                "employee", "specialization", "degree", "school"
            )
            .order_by("order")
        )
    
    def _get_exchange_rates_manager(self):

        from apps.exchange_rates.models import ExchangeRate
        
        return (
             ExchangeRate
             .objects
             .filter(
                currency__name=OuterRef("currency")
             ).order_by("-date")
        )

