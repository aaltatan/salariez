from .models import Employee
from .managers import EmployeeManager


class EmployeeProxy(Employee):
    objects = EmployeeManager()

    class Meta:
        proxy = True