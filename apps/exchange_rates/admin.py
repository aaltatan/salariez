from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from . import models

from apps.base import admin_actions


@admin.action(description="Reslugify selected exchange rate")
def reslugify_action(modeladmin, request, queryset):
    admin_actions.reslugify_action(request, queryset)


@admin.register(models.ExchangeRate)
class ExchangeRateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        "id", "currency", "rate", "date", "bulletin_number"
    ]
    search_fields = ["currency__name"]
    list_filter = ['currency']
    list_per_page = 20