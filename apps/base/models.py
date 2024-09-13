from django.db import models

from . import validators

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
    
    class Meta:
        abstract = True