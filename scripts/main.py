from apps.employees.models import Contract

from icecream import ic

def run() -> None:

    contracts = Contract.objects.all()
    for obj in contracts:
        ic(obj)
        ic(obj.salary)
        ic(obj.local_salary)