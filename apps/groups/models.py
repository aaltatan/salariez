from django.db.models.signals import pre_save

from apps.base import models as base_models, utils


class Group(base_models.AbstractNameModel):

    class Meta:
        ordering = ['name']
        permissions = [
            ['can_export', 'Can export data']
        ]


def group_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(group_pre_save, Group)