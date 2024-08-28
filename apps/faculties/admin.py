from django.contrib import admin
from django.utils.text import slugify
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from . import models


@admin.action(description="Reslugify selected faculties")
def reslugify_action(modeladmin, request, queryset):

    for obj in queryset:
        obj.slug = slugify(obj.name, allow_unicode=True)
        obj.save()

    messages.success(
        request, _("all selected faculties has been reslugifed successfully")
    )


@admin.register(models.Faculty)
class FacultyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}
    actions = [reslugify_action]