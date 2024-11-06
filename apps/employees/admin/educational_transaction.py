from django.contrib import admin

from ..models import EducationTransaction

from import_export.admin import ImportExportActionModelAdmin
from apps.base.admin import CustomDjangoQLSearchMixin


@admin.register(EducationTransaction)
class EducationTransactionAdmin(
    CustomDjangoQLSearchMixin, ImportExportActionModelAdmin, admin.ModelAdmin
):
    raw_id_fields = [
        'employee', 
        'degree',
        'specialization',
        'school',
    ]
    list_display = [
        'employee', 
        'degree',
        'specialization',
        'school',
        'order',
        'is_current',
    ]
    list_per_page = 10
    search_fields = ['employee']