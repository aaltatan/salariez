from django.contrib import admin

from . import models


@admin.register(models.Faculty)
class FacultyAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['name']
    }