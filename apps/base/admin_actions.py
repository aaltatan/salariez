from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


def reslugify_action(request, queryset):

    for obj in queryset:
        obj.slug = slugify(obj.name, allow_unicode=True)
        obj.save()

    messages.success(
        request, _("all ({}) selected object(s) has been reslugifed successfully").format(queryset.count())
    )