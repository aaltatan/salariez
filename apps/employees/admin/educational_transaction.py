from django.contrib import admin

from ..models import EducationTransaction


@admin.register(EducationTransaction)
class EducationTransactionAdmin(admin.ModelAdmin):
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