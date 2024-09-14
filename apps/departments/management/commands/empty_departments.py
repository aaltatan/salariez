from django.core.management.base import BaseCommand
from ...utils import empty_departments

class Command(BaseCommand):
  
    help = "empty departments table from database"

    def handle(self, *args, **kwargs) -> None:
      empty_departments()