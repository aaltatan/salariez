from django.db import models
from django.db.models import Count

from .mixins import QuerySetManagerMixin


class EmployeeManager(QuerySetManagerMixin, models.Manager):

    def get_counts_grouped_by(self, group_by: str = 'gender'):
        return self.get_queryset().values(group_by).annotate(
            counts=Count('pk')
        )