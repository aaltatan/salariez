from django.contrib import admin
from django.utils.html import format_html

from .models import Activity

from apps.base.utils.generic import dict_to_css
from apps.base.admin import CustomDjangoQLSearchMixin


@admin.register(Activity)
class ActivityAdmin(CustomDjangoQLSearchMixin, admin.ModelAdmin):

    @admin.display(description='formatted type')
    def formatted_type(self, obj):

        colors = {
            'create': 'green',
            'update': 'blue',
            'delete': 'red',
        }
        styles = {
            'color': 'white',
            'border-radius': '0.25rem',
            'padding': '0.25rem 0.5rem',
            'text-transform': 'capitalize',
            'font-weight': 'bolder'
        }

        styles['background-color'] = colors.get(obj.type.lower(), 'blue')
        styles = dict_to_css(styles)

        return format_html(f"<div style='{styles}'>{obj.type}</div>")

    list_display = [
        'created_at',
        'user',
        'type',
        'formatted_type',
        'old_data',
        'notes',
        'content_type',
        'content_object',
    ]

    list_per_page = 10
    list_filter = ['content_type', 'type']
    search_fields = ['user__username', 'notes']