from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models import Value, F
from django.db.models.functions import Concat
from django.db.models.signals import pre_save

from mptt.models import MPTTModel, TreeForeignKey

from . import utils

from apps.base import validators, utils as base_utils
from apps.cost_centers import models as cc_models


class SearchManager(models.Manager):
    
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().annotate(
            search=Concat(
                F('name'), 
                Value(' '), 
                F('department_id'), 
                Value(' '), 
                F('name'),
                Value(' '), 
                F('department_id'), 
            ),
        )


class Department(MPTTModel):
    
    department_id = models.CharField(
        name=_('department_id'),
        max_length=255,
        unique=True,
        validators=[validators.numeric_validator],
        default='',
        blank=True
    )
    name = models.CharField(
        name=_('name'),
        max_length=255,
        validators=[validators.four_chars_validator],
        help_text=_('name must be more than 3 chars')
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        null=True,
        blank=True,
        allow_unicode=True,
    )
    description = models.TextField(
        name=_('description'),
        blank=True,
        default='',
    )
    parent = TreeForeignKey(
        'self', 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='children'
    )
    cost_center = models.ForeignKey(
        cc_models.CostCenter,
        on_delete=models.PROTECT,
        related_name='departments',
        verbose_name=_('cost center')
    )
    
    objects = SearchManager()
            
    @property
    def get_create_path(self) -> str:
        return reverse('departments:create')
    
    @property
    def get_delete_path(self) -> str:
        return reverse('departments:delete', kwargs={'slug': self.slug})
    
    @property
    def get_update_path(self) -> str:
        return reverse('departments:update', kwargs={'slug': self.slug})
    
    def __str__(self) -> str:
        return self.name
    
    class MPTTMeta:
        order_insertion_by = ['department_id']
        
    class Meta:
        ordering = ['department_id']
        permissions = [
            ['can_export', 'Can export data']
        ]


def department_pre_save(sender, instance, *args, **kwargs):
    base_utils.slugify_instance(instance)
    utils.generate_department_id(instance)

pre_save.connect(department_pre_save, Department)