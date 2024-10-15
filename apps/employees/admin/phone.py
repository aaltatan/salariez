from django.contrib import admin

from ..models import Phone


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['employee', 'phone']
    list_per_page = 10
    search_fields = ['phone']