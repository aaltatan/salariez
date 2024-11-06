from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from . import models

from apps.base import admin_actions
from apps.base.admin import CustomDjangoQLSearchMixin


@admin.action(description="Reslugify selected departments")
def reslugify_action(modeladmin, request, queryset):
    admin_actions.reslugify_action(request, queryset)


@admin.register(models.Department)
class DepartmentAdmin(CustomDjangoQLSearchMixin, MPTTModelAdmin):
    
    ordering = ['department_id']
    list_display = [
        'name', 'id', 'department_id', 'slug', 'description'
    ]
    prepopulated_fields = {
        'slug': ['name']
    }
    raw_id_fields = ['parent']
    search_fields = ['name', 'description']
    actions = [reslugify_action]