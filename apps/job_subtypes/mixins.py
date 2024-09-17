from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from apps.base.mixins.bulk import BulkActionMixin


class BulkDeleteMixin(BulkActionMixin):

    bulk_content_template_path = 'partials/bulk-contents/delete.html'
    bulk_path = 'job_subtypes:bulk-delete'

    def modal_action(self, pks: list[int]):
        qs = self.model.objects.filter(pk__in=pks)
        for obj in qs:
            if 1 == 2:
                messages.error(
                    self.request, 
                    _('you can\'t delete this ({}) because there is one or more models related to it.').format(obj.name),
                )
            else:
                obj.delete()
                messages.success(
                    self.request, 
                    _('{} has been deleted successfully').format(obj.name)
                )


class CannotDeleteMixin:
    
    def cannot_delete(self, request, *args, **kwargs):
        
        model = self._get_model_class()
        instance = get_object_or_404(model, slug=kwargs.get('slug'))
        
        if 1 == 2:
            response = HttpResponse('')
            messages.error(
                request, 
                _('you can\'t delete this ({}) because there is one or more models related to it.').format(instance.name),
            )
            response['Hx-Retarget'] = '#no-content'
            response['Hx-Reswap'] = 'innerHTML'
            return response
        
        return None