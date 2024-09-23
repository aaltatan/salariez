from django.contrib import admin

from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):

    list_display = [
        'created_at',
        'user',
        'type',
        'new_data',
        'old_data',
        'notes',
        'content_type',
        'content_object',
    ]
