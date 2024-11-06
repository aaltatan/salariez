from django.contrib import admin

from ..models import Email

from import_export.admin import ImportExportActionModelAdmin
from apps.base.admin import CustomDjangoQLSearchMixin


@admin.register(Email)
class EmailAdmin(
    CustomDjangoQLSearchMixin, ImportExportActionModelAdmin, admin.ModelAdmin
):
    list_display = ['employee', 'email']
    list_per_page = 10
    search_fields = ['email']
