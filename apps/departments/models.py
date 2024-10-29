from django.db import models
from django.utils.translation import gettext as _
from django.db.models.signals import pre_save
from django.db.models.fields.generated import GeneratedField
from django.db.models.functions import Concat

from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from . import utils

from apps.base import validators, utils as base_utils, models as base_models
from apps.cost_centers import models as cc_models


class DepartmentManager(TreeManager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_related(
            'cost_center', 'parent'
        )


class Department(MPTTModel, base_models.AbstractNameModel):
    
    department_id = models.CharField(
        name=_('department_id'),
        max_length=255,
        unique=True,
        validators=[validators.numeric_validator],
        default='',
        blank=True,
        help_text=_('if you leave it blank, it will be filled based on parent id serial.'),
    )
    parent = TreeForeignKey(
        'self', 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='children',
        help_text=_('parent department if exists.'),
    )
    cost_center = models.ForeignKey(
        cc_models.CostCenter,
        on_delete=models.PROTECT,
        related_name='departments',
        verbose_name=_('cost center'),
        help_text=_('the cost center which belongs to'),
    )
    search = GeneratedField(
        expression=Concat(
            models.F('department_id'), 
            models.Value(' '), 
            models.F('name'), 
            models.Value(' '), 
            models.F('department_id'), 
            models.Value(' '), 
            models.F('name'), 
        ),
        output_field=models.CharField(max_length=255),
        db_persist=False,
    )

    objects = DepartmentManager()
    
    class MPTTMeta:
        level_attr = 'level'
        order_insertion_by=['department_id']
        
    class Meta:
        permissions = [
            ['can_export', 'Can export data']
        ]


def department_pre_save(sender, instance, *args, **kwargs):
    base_utils.slugify_instance(instance)
    utils.generate_department_id(instance)

pre_save.connect(department_pre_save, Department)