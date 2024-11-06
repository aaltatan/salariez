from django.contrib import admin

from ..models import Phone

from import_export.admin import ImportExportActionModelAdmin
from apps.base.admin import CustomDjangoQLSearchMixin


@admin.register(Phone)
class PhoneAdmin(
    CustomDjangoQLSearchMixin, ImportExportActionModelAdmin, admin.ModelAdmin
):
    list_display = ['employee', 'phone']
    list_per_page = 10
    search_fields = ['phone']