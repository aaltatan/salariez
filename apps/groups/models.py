from django.urls import reverse
from django.db.models.signals import pre_save

from apps.base import models as base_models, utils


class Group(base_models.AbstractNameModel):

    @property
    def get_absolute_path(self):
        index_path = reverse('employees:index')
        return f'{index_path}?groups={self.pk}'

    class Meta:
        ordering = ['name']
        permissions = [
            ['can_export', 'Can export data']
        ]


def group_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(group_pre_save, Group)