from django.db.models import F, Q
from django.db.models.functions import FirstValue

from icecream import ic

from apps.employees.models import Employee


def run() -> None:
   
   qs = Employee.objects.annotate(
      current_education=F('education_transactions__is_current'),
      school=F('education_transactions__school__name'),
      degree=F('education_transactions__degree__name'),
      specialization=F('education_transactions__specialization__name'),
      is_specialist=F('education_transactions__specialization__is_specialist'),
   ).filter(Q(current_education=None) | Q(current_education=True))[:20]

   for obj in qs:
      ic(
         obj.fullname, 
         obj.current_education, 
         obj.school,
         obj.degree,
         obj.specialization,
         obj.is_specialist,
      )