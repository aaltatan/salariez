from django.db.models import Subquery, OuterRef, Value
from django.db.models.functions import Coalesce

from icecream import ic

from apps.employees.models import Employee, EducationTransaction


def run() -> None:
   
   transactions = (
      EducationTransaction
      .objects
      .filter(is_current=True, employee=OuterRef('pk'))
      .select_related('employee', 'specialization', 'degree', 'school')
      .order_by('order')
   )

   qs = (
      Employee
      .objects
      .annotate(
         school=Coalesce(
            Subquery(transactions.values('school__name')[:1]), Value('-')
         ),
         specialization=Coalesce(
            Subquery(transactions.values('specialization__name')[:1]), Value('-')
         ),
         degree=Coalesce(
            Subquery(transactions.values('degree__name')[:1]), Value('-')
         ),
         is_academic=Coalesce(
            Subquery(transactions.values('degree__is_academic')[:1]), False
         ),
         is_specialist=Coalesce(
            Subquery(transactions.values('specialization__is_specialist')[:1]), False
         ),
         graduation_date=Subquery(transactions.values('graduation_date')[:1]),
      )
   )[:20]

   for obj in qs:
      ic(
         obj.fullname,
         obj.school,
         obj.specialization,
         obj.degree,
         obj.is_academic,
         obj.graduation_date,
         obj.is_specialist,
      )





# def run() -> None:
#    qs = Employee.objects.annotate(
#       current_education=(
#          Coalesce(
#             F('education_transactions__is_current'), True
#          )
#       ),
#       school=Coalesce(
#          F('education_transactions__school__name'), Value('-')
#       ),
#       degree=Coalesce(
#          F('education_transactions__degree__name'), Value('-')
#       ),
#       specialization=Coalesce(
#          F('education_transactions__specialization__name'), Value('-')
#       ),
#       is_specialist=Coalesce(
#          F('education_transactions__specialization__is_specialist'), 
#          False,
#       ),
#    ).filter(current_education=True)[:20]


#    for obj in qs:
#       ic(
#          obj.fullname, 
#          obj.current_education, 
#          obj.school,
#          obj.degree,
#          obj.specialization,
#          obj.is_specialist,
#       )