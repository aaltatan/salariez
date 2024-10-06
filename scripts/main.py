from django.db import models
from django.db.models import Count, Q, ExpressionWrapper, F, Value
from django.db.models.functions import Round

from apps.employees.models import Employee


def run() -> None:

    qs = Employee.objects.aggregate(
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

    print(qs)