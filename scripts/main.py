from django.utils import timezone

from apps.employees.models import Employee

from icecream import ic

def run() -> None:

    today = timezone.now().date()

    qs = Employee.objects.filter(
        hire_date__gt=today - timezone.timedelta(days=90)
    )

    ic(qs.count())