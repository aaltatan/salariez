from django.db.models.signals import pre_save

from apps.base import models as base_models, utils


class SchoolType(base_models.AbstractNameModel):

    class Meta:
        ordering = ['name']
        permissions = [
            ['can_export', 'Can export data']
        ]


def school_type_pre_save(sender, instance, *args, **kwargs):
    utils.slugify_instance(instance)

pre_save.connect(school_type_pre_save, SchoolType)