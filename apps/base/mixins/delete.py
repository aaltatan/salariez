import json
from abc import ABC, abstractmethod

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.urls import reverse

from . import utils


class AbstractDelete(ABC):
    
    @property
    @abstractmethod
    def model(self): ...
    
    @property
    @abstractmethod
    def deleter(self): ...
    

class DeleteMixin(utils.HelperMixin, AbstractDelete):
    
    """
    utility class to implement delete record functionality.  
    
    ### required attributes:  
    - `model: Model`  
    - `deleter: Deleter`  
    
    ### optional attributes:  
    - `modal_template_name: str` like: `'partials/delete-modal.html'`
    - `hx_location_path: str` like: `'<app_name>:index'`
    - `hx_location_target: str` like: `'#<app_name>-table'`
     
    """
    
    def get(self, request, *args, **kwargs):
        
        instance = get_object_or_404(
            self.model, slug=kwargs.get('slug')
        )
        
        message = (
            _('are you sure you want to {}delete{} {} ?')
            .format(
                '<span class="text-[red] uppercase underline font-bold">',
                '</span>',
                instance, 
            )
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
        
        instance = get_object_or_404(
            self.model, slug=kwargs.get('slug')
        )
        
        self.deleter(instance, request).delete()
        
        hx_location = {
            'path': reverse(self._get_hx_location_path()),
            'values': {**request.POST},
            'target': self._get_hx_location_target(),
        }
        
        response = HttpResponse('')
        response['Hx-Location'] = json.dumps(hx_location)
        response['Hx-Trigger'] = 'get-messages'
        
        return response