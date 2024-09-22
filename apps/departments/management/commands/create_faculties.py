from django.core.management.base import BaseCommand

from ... import models, utils
from apps.cost_centers import models as cc_models

class Command(BaseCommand):
  
    help = "create faculties based on WPU facts"

    def handle(self, *args, **kwargs) -> None:
      utils.create_departments(
         model=models.Department, cc_model=cc_models.CostCenter
      )