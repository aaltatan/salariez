from django.db import models


class OptimizationsMixin:
    
    def _select_related(self, qs: models.QuerySet) -> models.QuerySet:
        return qs.select_related('area', 'nationality')
    
    def _prefetch_related(self, qs: models.QuerySet) -> models.QuerySet:
        return qs.prefetch_related(
            'mobiles', 'phones', 'emails', 'education_transactions', 'groups'
        )
