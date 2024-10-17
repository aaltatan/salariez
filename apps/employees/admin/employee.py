from django.contrib import admin

from .tabular import (
    MobileTabular, 
    EmailTabular, 
    PhoneTabular, 
    EducationTransactionTabular,
)
from ..proxies import EmployeeProxy


@admin.register(EmployeeProxy)
class EmployeeAdmin(admin.ModelAdmin):
    
    inlines = [
        MobileTabular, 
        EmailTabular, 
        PhoneTabular,
        EducationTransactionTabular,
    ]
    raw_id_fields = [
        'area', 'department', 'position'
    ]
    list_per_page = 10
    search_fields = ['firstname', 'lastname', 'father_name']
    list_display = [
        'firstname',
        'lastname',
        'father_name',
        'mother_name',
        'national_id',
        'department',
        'gender',
    ]
    fields = [
        ('profile',),
        ('identity_document',),
        ('firstname', 'lastname', 'father_name', 'mother_name',),
        ('birth_place', 'birth_date',),
        ('national_id',),
        ('card_id',),
        ('civil_registry_office',),
        ('registry_office_name', 'registry_office_id',),
        ('gender', 'face_color', 'eyes_color',),
        ('address', 'special_signs', 'card_date',),
        ('martial_status', 'military_status', 'religion',),
        ('nationality', 'area', 'current_address',),
        ('department', 'position', 'job_subtype',),
        ('status', 'hire_date', 'institution_id',),
        ('salary',),
        ('slug',),
        ('notes',),
    ]
    prepopulated_fields = {
        'slug': ['firstname', 'father_name', 'lastname', 'national_id']
    }