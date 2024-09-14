from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


class CannotDeleteFacultyMixin:
    
    def cannot_delete(self, request, *args, **kwargs):
        
        instance = get_object_or_404(self.model, slug=kwargs.get('slug'))
        
        qs = instance.children.all()
        
        if qs.exists():
            response = HttpResponse('')
            messages.error(
                request, 
                _('you can\'t delete this ({}) because it has a children departments').format(instance.name),
            )
            response['Hx-Retarget'] = '#no-content'
            response['Hx-Reswap'] = 'innerHTML'
            return response
        
        return None