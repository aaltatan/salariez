from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from apps.base.mixins.bulk import AbstractBulkAction


class BulkDeleteMixin(AbstractBulkAction):

    def modal_action(self, pks: list[int]):
        qs = self.model.objects.filter(pk__in=pks)
        for obj in qs:
            if obj.departments.all().exists():
                messages.error(
                    self.request, 
                    _('you can\'t delete this ({}) because there is one or more models related to it.').format(obj.name),
                )
            else:
                obj.delete()
                messages.success(self.request, _('{} has been deleted successfully').format(obj.name))

    def get_bulk_path(self):
        return reverse('cost_centers:bulk-delete')
    
    def get_modal_content(self):
        
        pks = self.get_get_pks()
        context = {
            'qs': self.model.objects.filter(pk__in=pks)
        }
        return render_to_string(
            'apps/cost_centers/partials/bulk-contents/delete.html',
            context,
            self.request
        )


class CannotDeleteMixin:
    
    def cannot_delete(self, request, *args, **kwargs):

        model = self._get_model_class()
        instance = get_object_or_404(model, slug=kwargs.get('slug'))
        
        criteria = instance.departments.all().exists()
        
        if criteria:
            response = HttpResponse('')
            messages.error(
                request, 
                _('you can\'t delete this ({}) because there is one or more models related to it.').format(instance.name),
            )
            response['Hx-Retarget'] = '#no-content'
            response['Hx-Reswap'] = 'innerHTML'
            return response
        
        return None