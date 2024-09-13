from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from . import models

from apps.base import admin_actions


@admin.action(description="Reslugify selected faculties")
def reslugify_action(modeladmin, request, queryset):
    admin_actions.reslugify_action(modeladmin, request, queryset)


@admin.register(models.JobSubtype)
class JobSubtypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["name", "job_type", "slug"]
    prepopulated_fields = {"slug": ["name"]}
    actions = [reslugify_action]