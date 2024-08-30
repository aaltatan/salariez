from abc import ABC, abstractmethod

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from . import utils

class AbstractSearch(ABC):
    
    @property
    @abstractmethod
    def input_placeholder(self): ...
    
    @property
    @abstractmethod
    def model(self): ...


class SearchMixin(utils.HelperMixin, AbstractSearch):
    
    """
    utility class for implement search for record functionality.  
    you need to set those attributes on derived class:  
    - `model: Model`
    - `input_placeholder: str` like `search faculties`
    optional attributes:  
        - `search_path: str` like reverse('faculties:search')
        - `template_name: str` like `apps/<app_label>/partials/search-results.html`
    """
    
    def _get_search_path(self):
        
        search_path = getattr(self, 'search_path', None)
        
        if search_path is None:
            app_label = self.get_app_label()
            search_path = reverse(f'{app_label}:search')
            
        return search_path
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        name = request.GET.get('name')
        id = request.GET.get('id')
        
        obj = None
        if id:
            obj = get_object_or_404(self.model, id=int(id))
        
        placeholder = request.GET.get('placeholder')
        if placeholder is None:
            placeholder = self.input_placeholder
        
        search_path = self._get_search_path()
        
        context = {
            'path': search_path,
            'placeholder': placeholder,
            'name': name,
            'obj': obj,
            'id': id,
        } 
        
        return render(request, 'components/inputs/search.html', context)
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        q = request.POST.get('q', '')
        context = {
            'path': self._get_search_path()
        }
        
        if q is None or q == '':
            context['qs'] = self.model.objects.none()
        else:
            context['qs'] = self.model.objects.filter(search__contains=q)
            
        template_name = getattr(self, 'search_results_template', None)
        
        if template_name is None:
            app_label = self.get_app_label()
            template_name = f'apps/{app_label}/partials/search-results.html'
        
        return render(request, template_name , context)