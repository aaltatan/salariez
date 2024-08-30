from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models.signals import pre_save

from mptt.models import MPTTModel, TreeForeignKey

from apps.base import validators, managers, utils


class Department(MPTTModel):
    
    name = models.CharField(
        name=_('name'),
        max_length=255,
        validators=[validators.four_chars],
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
    
    objects = managers.SearchManager()
    
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
        order_insertion_by = ['id']
        
    class Meta:
        permissions = [
            ['can_export', 'Can export data']
        ]
        

def faculty_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(faculty_pre_save, Department)