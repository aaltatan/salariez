import re
import json
from abc import ABC, abstractmethod
from urllib.parse import urlencode

from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, render
from django.urls import reverse

from . import utils


class AbstractBulkAction(ABC):
    
    @property
    @abstractmethod
    def modal_action(self): ...
    
    @property
    @abstractmethod
    def get_bulk_path(self): ...
    
    @property
    @abstractmethod
    def get_modal_content(self): ...


class AbstractBulkModal(ABC):
    
    @property
    @abstractmethod
    def model(self): ...


class AbstractBulkMapper(ABC):
    
    @property
    @abstractmethod
    def mapper(self): ...


class BulkMapperMixin(AbstractBulkMapper):
    """
    utility class to implement redirection between bulk template and bulk action.  
    ### required attributes:  
    - `mapper: dict`  
    """
    
    def get(self, request: HttpRequest, *args, **kwargs):
        url = self.get_redirect_url()
        querystring = urlencode(request.GET)
        full_url = f'{url}?{querystring}'
        return redirect(full_url)
    
    def get_redirect_url(self, *args, **kwargs) -> str | None:
        
        for key in self.request.GET.keys():
            if self.mapper.get(key):
                return reverse(self.mapper[key])


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
        
        response = render(request, 'partials/confirm-modal.html', context)
        response['Hx-Retarget'] = '#modal'
        return response
    
    def post(self, request: HttpRequest):
        
        response = HttpResponse('')
        
        pks = [
            int(pk) for pk in self.request.POST.get('pks').split(",")
        ]
        
        # action & message
        self.modal_action(pks)
        
        hx_location = {
            'path': reverse(self._get_hx_location_path()),
            'values': {**request.POST},
            'target': self._get_hx_location_target(),
        }
        response['Hx-Location'] = json.dumps(hx_location)
            
        return response