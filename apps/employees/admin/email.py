from django.contrib import admin

from ..models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['employee', 'email']
    list_per_page = 10
    search_fields = ['email']
