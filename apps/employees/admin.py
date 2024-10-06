from django.contrib import admin

from .models import Mobile, Employee, Email, Phone


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['employee', 'email']
    list_per_page = 10
    search_fields = ['email']


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['employee', 'phone']
    list_per_page = 10
    search_fields = ['phone']


@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ['employee', 'mobile', 'has_whatsapp']
    list_per_page = 10
    search_fields = ['mobile']
    list_filter = ['has_whatsapp']


class EmailInline(admin.TabularInline):

    model = Email
    fields = ['email', 'notes']
    extra = 0


class MobileInline(admin.TabularInline):
    
    model = Mobile
    fields = ['mobile', 'has_whatsapp', 'notes']
    extra = 0


class PhoneInline(admin.TabularInline):
    
    model = Phone
    fields = ['phone', 'notes']
    extra = 0


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    
    inlines = [
        MobileInline, EmailInline, PhoneInline,
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
        ('profile'),
        ('identity_document'),
        ('firstname', 'lastname', 'father_name', 'mother_name'),
        ('birth_place', 'birth_date'),
        ('national_id'),
        ('card_id'),
        ('civil_registry_office'),
        ('registry_office_name', 'registry_office_id'),
        ('gender', 'face_color', 'eyes_color'),
        ('address', 'special_signs', 'card_date'),
        ('martial_status', 'military_status'),
        ('nationality', 'area'),
        ('department', 'position', 'job_subtype'),
        ('job_status', 'status', 'hire_date', 'institution_id'),
        ('salary'),
        ('slug'),
        ('notes'),
    ]
    prepopulated_fields = {
        'slug': ['firstname', 'father_name', 'lastname', 'national_id']
    }