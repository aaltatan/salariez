from apps.employees.models import Employee

from icecream import ic

def run() -> None:

    qs = Employee.objects.values('civil_registry_office')
    civil_registry_offices = list(set([
        obj['civil_registry_office'] for obj in qs
    ]))
    ic(civil_registry_offices)