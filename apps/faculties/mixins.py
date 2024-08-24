from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from apps.base.mixins.bulk import AbstractBulkAction


class BulkDeleteMixin(AbstractBulkAction):

    def modal_action(self, pks: list[int]):
        self.model.objects.filter(pk__in=pks).delete()
        messages.info(self.request, _('done'), 'bg-green-600')

    def get_bulk_path(self):
        return reverse('faculties:bulk-delete')
    
    def get_modal_content(self):
        
        pks = self.get_get_pks()
        
        context = {
            'qs': self.model.objects.filter(pk__in=pks)
        }
        
        return render_to_string(
            'apps/faculties/partials/bulk-contents/delete.html',
            context,
            self.request
        )


class CannotDeleteFacultyMixin:
    
    def cannot_delete(self, request, *args, **kwargs):
        
        instance = get_object_or_404(self.model, slug=kwargs.get('slug'))
        
        if 1 == 2:
            response = HttpResponse('')
            messages.info(
                request, 
                _('you can\'t delete this ({}) because there is one or more models related to it.').format(instance.name),
                'bg-red-600'
            )
            response['Hx-Retarget'] = '#no-content'
            response['Hx-Reswap'] = 'innerHTML'
            return response
        
        return None