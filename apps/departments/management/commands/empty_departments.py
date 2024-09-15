from django.core.management.base import BaseCommand

from ... import models, utils

class Command(BaseCommand):
  
    help = "empty departments table from database"

    def handle(self, *args, **kwargs) -> None:
      utils.empty_departments(model=models.Department)