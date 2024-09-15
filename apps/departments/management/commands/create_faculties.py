from django.core.management.base import BaseCommand

from ... import models, utils

class Command(BaseCommand):
  
    help = "create faculties based on WPU facts"

    def handle(self, *args, **kwargs) -> None:
      utils.create_faculties(model=models.Department)