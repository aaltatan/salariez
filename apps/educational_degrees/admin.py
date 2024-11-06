from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from . import models

from apps.base import admin_actions
from apps.base.admin import CustomDjangoQLSearchMixin


@admin.action(description="Reslugify selected educational degrees")
def reslugify_action(modeladmin, request, queryset):
    admin_actions.reslugify_action(request, queryset)


@admin.register(models.EducationalDegree)
class EducationalDegreeAdmin(
    CustomDjangoQLSearchMixin, ImportExportModelAdmin, admin.ModelAdmin
):
    list_display = ["id", "name", "is_academic", "order", "slug"]
    search_fields = ["name"]
    list_per_page = 20
    prepopulated_fields = {"slug": ["name"]}
    actions = [reslugify_action]