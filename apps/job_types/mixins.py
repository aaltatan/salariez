import json

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.base.mixins.utils import HelperMixin
from apps.base.mixins.bulk import BulkActionMixin


class BulkDeleteMixin(BulkActionMixin):

    bulk_content_template_path = 'partials/bulk-contents/delete.html'
    bulk_path = 'job_types:bulk-delete'

    def modal_action(self, pks: list[int]):
        qs = self.model.objects.filter(pk__in=pks)
        for obj in qs:
            if obj.subtypes.all().exists():
                messages.error(
                    self.request, 
                    _('you can\'t delete this ({}) because there is one or more models related to it.').format(obj.name),
                )
            else:
                obj.delete()
                messages.success(self.request, _('{} has been deleted successfully').format(obj.name))


class CannotDeleteMixin(HelperMixin):
    
    def cannot_delete(self, request, *args, **kwargs):

        model = self._get_model_class()
        
        instance = get_object_or_404(model, slug=kwargs.get('slug'))
        
        criteria = instance.subtypes.all()
        
        if criteria.exists():
            messages.error(
                request, 
                _('you can\'t delete this ({}) because there is one or more models related to it.').format(instance.name),
            )
            response = HttpResponse('')
            hx_location = {
                'path': reverse(self._get_hx_location_path()),
                'values': {**request.POST},
                'target': self._get_hx_location_target(),
            }
            response['Hx-Location'] = json.dumps(hx_location)
            return response
        
        return None