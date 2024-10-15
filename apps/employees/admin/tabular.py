from django.contrib import admin

from ..models import Email, Mobile, Phone, EducationTransaction


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