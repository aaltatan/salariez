from typing import Literal

from django.db.models import Q
from ..utils.generic import parse_decimals


METHOD = Literal['contains']

class FiltersMixin:
    
    def _get_qs(
        self, qs, value, field, db_method: METHOD = 'contains'
    ):
        
        reversed: bool = value.startswith('!')

        if reversed:
            value = value[1:]

        kwargs = ' & '.join([
            f'Q({field}__{db_method}="{k}")'
            for k in value.split(" ")
        ])

        stmt = ~Q(eval(kwargs)) if reversed else Q(eval(kwargs))

        return qs.filter(stmt)
    
    def filter_parent(self, qs, name, value):

        if not value:
            return qs
        
        stmt = qs.none()
        for obj in value:
            stmt = obj.get_descendants() | stmt

        return stmt
    
    def filter_combobox(self, qs, name, value):
        if not value:
            return qs
        lookup = {f'{name}__in': value}
        return qs.filter(**lookup).distinct()

    def filter_decimals(self, qs, name, value):
        if value:
            lookup = {name: parse_decimals(value)}
            return qs.filter(**lookup)
        return qs

    def filter_numbers_and_dates(self, qs, name, value):
        if value:
            lookup = {name: value}
            return qs.filter(**lookup)
        return qs
    
    def filter_name(self, qs, name, value):
        return self._get_qs(qs, value, 'search')

    def filter_description(self, qs, name, value):
        return self._get_qs(qs, value, 'description')

    def filter_cost_center(self, qs, name, value):
        return self._get_qs(qs, value, 'cost_center_accounting_id')