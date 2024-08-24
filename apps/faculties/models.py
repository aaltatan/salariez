from django.db import models

from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models.signals import pre_save

from apps.base import validators, utils
from apps.base.managers import SearchManager


class Faculty(models.Model):
    
    name = models.CharField(
        verbose_name=_('faculty'),
        unique=True,
        max_length=255,
        help_text=_('faculty name must be more than 3 characters'),
        validators=[validators.four_chars]
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        null=True,
        blank=True,
        allow_unicode=True,
    )
    
    objects = SearchManager()
    
    class Meta:
        verbose_name_plural = _('faculties')
        ordering = ['name']
    
    @property
    def get_create_path(self):
        return reverse('faculties:create')
    
    @property
    def get_update_path(self):
        return reverse('faculties:update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_path(self):
        return reverse('faculties:delete', kwargs={'slug': self.slug})
    
    def __str__(self) -> str:
        return self.name


def faculty_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(faculty_pre_save, Faculty)