import re
import json
from abc import ABC, abstractmethod

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .. import utils


class AbstractBulkModal(ABC):
    
    @property
    @abstractmethod
    def model(self): ...


class BulkModalMixin(utils.HelperMixin, AbstractBulkModal):
    
    """
    utility class to implement modal appearance and its functionality.  
    you need to implement `modal_action`, `get_bulk_path` and `get_modal_content` methods for each (bulk mixin) class in `apps.<app_name>.mixin`.  
    
    ### optional attributes:  
    - `hx_location_path : str` like: `'<app_name>:index'`
    - `hx_location_target : str` like: `'#<app_name>-table'` 
    
    # Note:
    you need to set at least one bulk mixin locally in `apps.<app_name>.mixin` like `BulkDeleteMixin`
    
    """
    
    def get_get_pks(self):
        
        return [
            int(re.findall(r'\d+', k)[0]) 
            for k in self.request.GET.keys()
            if k.endswith('selected')
        ]
    
    def get(self, request: HttpRequest):
        
        context = {
            'pks': ",".join([str(pk) for pk in self.get_get_pks()]),
            'bulk_path': self.get_bulk_path(),
            'modal_content': self.get_modal_content()
        }
        
        response = render(request, 'partials/modals/confirm.html', context)
        response['Hx-Retarget'] = '#modal'
        return response
    
    def post(self, request: HttpRequest):
        
        response = HttpResponse('')
        
        pks = [
            int(pk) for pk in self.request.POST.get('pks').split(",")
        ]
        
        # action & message
        self.modal_action(pks, request)
        
        hx_location = {
            'path': reverse(self._get_hx_location_path()),
            'values': {**request.POST},
            'target': self._get_hx_location_target(),
            'select': self._get_hx_location_target(),
        }
        response['Hx-Location'] = json.dumps(hx_location)
        response['Hx-Trigger'] = 'get-messages'
            
        return response