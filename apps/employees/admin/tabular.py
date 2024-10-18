from django.contrib import admin

from ..models import (
    Email, Mobile, Phone, EducationTransaction, Contract
)


class EmailTabular(admin.TabularInline):
    model = Email
    fields = ['email', 'notes']
    extra = 0


class MobileTabular(admin.TabularInline):
    model = Mobile
    fields = ['mobile', 'has_whatsapp', 'notes']
    extra = 0


class PhoneTabular(admin.TabularInline):
    model = Phone
    fields = ['phone', 'notes']
    extra = 0


class EducationTransactionTabular(admin.TabularInline):
    model = EducationTransaction
    raw_id_fields = [
        'employee', 
        'degree', 
        'school', 
        'specialization', 
    ]
    fields = [
        'employee', 
        'degree', 
        'school', 
        'specialization', 
        'order',
        'graduation_date',
    ]
    extra = 0


class ContractTabular(admin.StackedInline):
    model = Contract
    raw_id_fields = [
        'employee', 
        'department', 
        'job_subtype', 
        'status', 
        'position', 
    ]
    fields = [
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
    extra = 0