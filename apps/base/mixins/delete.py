import json
from abc import ABC, abstractmethod

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.urls import reverse

from icecream import ic

from . import utils


class AbstractDelete(ABC):
    
    @property
    @abstractmethod
    def model(self): ...
    

class DeleteMixin(utils.HelperMixin, AbstractDelete):
    
    """
    utility class to implement delete record functionality.  
    
    # Note
    you need to implement `CannotDeleteMixin` class and `cannot_delete` method in it locally in `apps.<app_name>.mixins` to create cannot_delete functionality in case the object has been in relation with other models.
        
    ### required attributes:  
    - `model: Model`  
    
    ### optional attributes:  
    - `modal_template_name: str` like: `'partials/delete-modal.html'`
    - `hx_location_path: str` like: `'<app_name>:index'`
    - `hx_location_target: str` like: `'#<app_name>-table'`
     
    """
    
    def get(self, request, *args, **kwargs):
        
        if not hasattr(self, 'cannot_delete'):
            raise NotImplementedError('you need to implement cannot_delete method on your view')
        
        instance = get_object_or_404(self.model, slug=kwargs.get('slug'))
        
        instance_name = getattr(instance, 'name')
        
        message = (
            _('are you sure you want to delete {} ?')
            .format(instance_name)
        )
        
        context = {
            'instance': instance,
            'message': message,
            'delete_path': instance.get_delete_path,
            'page': request.GET.get('page'),
        }
        
        modal_template_name = self._get_modal_template_name()
        
        return render(request, modal_template_name, context)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        
        slug=kwargs.get('slug')
        
        instance = get_object_or_404(self.model, slug=slug)
        response = HttpResponse('')
        
        cannot_delete_response = self.cannot_delete(request, *args, **kwargs)
        
        if cannot_delete_response is not None:
            return cannot_delete_response
        
        instance.delete()
        messages.success(request, _('done'))
        
        hx_location = {
            'path': reverse(self._get_hx_location_path()),
            'values': {**request.POST},
            'target': self._get_hx_location_target(),
            'swap': 'outerHTML',
        }
        
        ic(hx_location)
        
        response['Hx-Location'] = json.dumps(hx_location)
        
        return response