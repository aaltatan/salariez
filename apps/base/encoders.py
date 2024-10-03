from typing import Any
from datetime import date
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder


class CustomJSONEncoder(DjangoJSONEncoder):

    def default(self, o: Any) -> Any:
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, Decimal):
            return float(o)
        return super().default()

