from django.db import models
from django.db.models import Value, F
from django.db.models.functions import Concat


class SearchManager(models.Manager):
    
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().annotate(
            search=Concat(F('name'), Value(' '), F('name')),
        )