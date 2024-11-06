from django.contrib import admin

from ..models import Mobile

from import_export.admin import ImportExportActionModelAdmin
from apps.base.admin import CustomDjangoQLSearchMixin


@admin.register(Mobile)
class MobileAdmin(
    CustomDjangoQLSearchMixin, ImportExportActionModelAdmin, admin.ModelAdmin
):
    list_display = ['employee', 'mobile', 'has_whatsapp']
    list_per_page = 10
    search_fields = ['mobile']
    list_filter = ['has_whatsapp']
