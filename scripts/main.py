from django.db.models.functions import Now, TruncDate
from django.db import models

from apps.employees.models import Employee


def run() -> None:

    qs = Employee.objects.annotate(
        test1=TruncDate(Now()),
        test=models.ExpressionWrapper(
            TruncDate(Now()) - models.F('birth_date'),
            output_field=models.DecimalField()
        ),
        test_age=models.F('test') / models.Value(86_400_000_000) / models.Value(365)
    )

    for obj in qs:
        print(obj.birth_date)
        print(obj.test_age)
        print('#' * 100)