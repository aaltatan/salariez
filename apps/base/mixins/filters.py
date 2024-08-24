from typing import Any

from django.db.models import Q
from django.utils.translation import gettext_lazy as _


ATTRS: dict[str, Any] = {
    "autocomplete": "off",
    "hx-target": "#container",
    "hx-select": "#container",
    "hx-swap": "outerHTML",
    "hx-include": "[data-include]",
    "x-on:keydown": """
        if ($event.code === 'Escape') {
            $el.value = '';
            document.getElementById('filter-submit-btn').click();
        }; 
    """
}

class FiltersMixins:

    def filter_name(self, queryset, name, value):
        keywords = value.split(" ")
        stmt = Q()
        for keyword in keywords:
            stmt &= Q(search__contains=keyword)
        return queryset.filter(stmt)
