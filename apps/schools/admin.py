from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from . import models

from apps.base import admin_actions


@admin.action(description="Reslugify selected schools")
def reslugify_action(modeladmin, request, queryset):
    admin_actions.reslugify_action(request, queryset)


@admin.register(models.School)
class SchoolAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    prepopulated_fields = {"slug": ["name"]}
    actions = [reslugify_action]