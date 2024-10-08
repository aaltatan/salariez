from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.utils.translation import gettext as _

from apps.base.encoders import CustomJSONEncoder


class Activity(models.Model):
    
    class TypeChoices(models.TextChoices):
        CREATE = 'create', _('create').title()
        UPDATE = 'update', _('update').title()
        DELETE = 'delete', _('delete').title()
        OTHER = 'other', _('other').title()

    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='activities'
    )
    type = models.CharField(
        max_length=255,
        choices=TypeChoices.choices,
        default=TypeChoices.CREATE,
    )
    old_data = models.JSONField(
        null=True, blank=True, encoder=CustomJSONEncoder
    )
    notes = models.CharField(max_length=255)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
        return f'Activity[{self.type}] @{self.user.username}'

    class Meta:
        ordering = ['-created_at', 'type']
        verbose_name_plural = 'activities'
