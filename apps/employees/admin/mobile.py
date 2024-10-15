from django.contrib import admin

from ..models import Mobile


@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ['employee', 'mobile', 'has_whatsapp']
    list_per_page = 10
    search_fields = ['mobile']
    list_filter = ['has_whatsapp']
