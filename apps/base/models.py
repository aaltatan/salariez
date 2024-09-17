from django.db import models
from django.urls import reverse

from . import validators, managers


class BaseTimeStampSoftDeleteModel(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        
    def delete(self):
        self.is_deleted = True
        self.save()


class AbstractNameModel(models.Model):
    
    name = models.CharField(
        max_length=255, 
        unique=True, 
        validators=[validators.four_chars_validator],
    )
    description = models.TextField(
        max_length=255, blank=True, default='',
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        null=True,
        blank=True,
        allow_unicode=True,
    )

    def __str__(self) -> str:
        return self.name

    objects = managers.SearchManager()

    def _get_app_label(self):
        return self.__class__._meta.app_label

    @property
    def get_create_path(self):
        return reverse(f'{self._get_app_label()}:create')

    @property
    def get_update_path(self):
        return reverse(
            f'{self._get_app_label()}:update', kwargs={'slug': self.slug}
        )
    
    @property
    def get_delete_path(self):
        return reverse(
            f'{self._get_app_label()}:delete', kwargs={'slug': self.slug}
        )
    
    class Meta:
        abstract = True