from django.core.management.base import BaseCommand
from apps.departments.models import Department


class Command(BaseCommand):
  
    help = "empty departments table from database"

    def handle(self, *args, **kwargs) -> None:
      
      qs = Department.objects.all()
      
      if not qs.exists():
        print('all departments has been deleted successfully')
        return
      
      criteria = [obj.delete() for obj in qs if obj.is_leaf_node()]
      
      if criteria:
          return self.handle(*args, **kwargs)