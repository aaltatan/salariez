from abc import ABC, abstractmethod
from urllib.parse import urlencode

from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse


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
        for key in self.request.GET:
            if self.mapper.get(key):
                return reverse(self.mapper[key])