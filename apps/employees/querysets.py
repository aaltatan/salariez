from django.db import models
from django.utils import timezone


class EmployeeQuerySet(models.QuerySet):

    def today_birthdays(self):
        return self.filter(
            birth_date__day=timezone.now().day,
            birth_date__month=timezone.now().month,
        )
    
    def this_month_birthdays(self, upcoming_only: bool = True):
        
        filters = {
            'birth_date__month': timezone.now().month,
        }

        if upcoming_only:
            filters['birth_date__day__gt'] = timezone.now().day
            
        return self.filter(**filters)
