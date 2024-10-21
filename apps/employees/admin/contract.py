from django.contrib import admin

from ..models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    raw_id_fields = [
        'employee', 
        'department', 
        'job_subtype', 
        'status', 
        'position', 
    ]
    list_display = [
        'employee', 
        'department', 
        'job_subtype', 
        'status', 
        'position', 
        'contract_type', 
        'ownership', 
        'salary', 
        'start_date', 
        'end_date', 
        'institution_id', 
    ]
    list_per_page = 10
    search_fields = ['employee']