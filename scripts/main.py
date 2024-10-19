from django.db.models import Window, RowRange, F
from django.db.models.functions import LastValue
from icecream import ic

from apps.employees.models import Contract, Employee

def run():
  
  emp = Employee.objects.get(pk=935)
  qs = Contract.objects.annotate(
    next_start_date=Window(
      expression=LastValue('start_date'),
      frame=RowRange(start=None, end=1),
      order_by=F('pk').asc()
    )
  ).filter(employee=emp).order_by('pk')

  for obj in qs:
    ic(
      obj, 
      obj.employee.fullname, 
      obj.start_date, 
      obj.next_start_date,
    )