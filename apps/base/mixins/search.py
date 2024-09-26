import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from inspect import signature

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Q

from . import utils


@dataclass
class Attrs:
    name: str | None = None
    value: str | None = None
    id: str | None = None
    placeholder: str | None = None
    required: str | None = None
    multiple: str | None = None
    
    @classmethod
    def from_request(cls, **kwargs):
        fields = signature(cls).parameters
        return cls(**{k:v[0] for k,v in kwargs.items() if k in fields})
    
    def __post_init__(self):
        self.required = self.required == 'true'
        self.multiple = self.multiple == 'true'
        if self.id:
            self.id = int(self.id)


class AbstractSearch(ABC):
    
    @property
    @abstractmethod
    def model(self): ...
    
    @property
    @abstractmethod
    def input_placeholder(self): ...


class SearchMixin(utils.HelperMixin, AbstractSearch):
    
    """
    utility class for implement search for record functionality.  
    ### required attributes:  
    - `model: Model`
    - `input_placeholder: str` like `search faculties`
    ### optional attributes:  
    - `search_container_id: str` like `search-container`
    - `search_path: str` like reverse('faculties:search')
    - `template_name: str` like `apps/<app_label>/partials/search-results.html`
    """

    def _get_container_id(self):

        if getattr(self, 'search_container_id', None) is not None:
            return self.search_container_id

        app_label = self._app_label_to_kebab(self._get_app_label())
        return f'{app_label}-search-container'
    
    def _get_search_path(self):
        
        search_path = getattr(self, 'search_path', None)
        
        if search_path is None:
            app_label = self._get_app_label()
            search_path = reverse(f'{app_label}:search')
            
        return search_path
    
    def get_queryset(self):
        return self.get_manager().all()
    
    def get_manager(self):
        return self.model.objects
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        attrs = Attrs.from_request(**request.GET)

        if attrs.placeholder is None:
            attrs.placeholder = self.input_placeholder
        
        obj = None

        if attrs.id:
            obj = get_object_or_404(self.model, id=attrs.id)

        search_path = self._get_search_path()

        context = {
            'path': search_path,
            **attrs.__dict__,
            'obj': obj,
            'container_id': self._get_container_id()
        } 

        template = 'components/inputs/search.html'
        criteria = request.GET.get('multiple')
        if criteria:
            options = self.model.objects.all()
            options = [
                {
                    'value': option.id, 
                    'text': str(option), 
                    'selected': False, 
                    'show': True
                } 
                for option in options
            ]
            context['options'] = json.dumps(options)
            template = 'components/inputs/combo.html'
        
        return render(request, template, context)
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        attrs = Attrs.from_request(**request.GET)

        q = {
            k: v for k,v in request.POST.items() 
            if k.startswith('q-') and v != ''
        }
        q = list(q.values())
        q = q[0] if len(q) else ''

        context = {
            **attrs.__dict__,
            'path': self._get_search_path(),
            'container_id': self._get_container_id()
        }

        qs = self.get_queryset()
        
        if q is None or q == '':
            context['qs'] = self.model.objects.none()
        else:
            keywords = q.split(" ")
            stmt = Q()
            for keyword in keywords:
                stmt &= Q(search__contains=keyword)
            context['qs'] = qs.filter(stmt)
            
        template_name = getattr(self, 'search_results_template', None)
        
        if template_name is None:
            app_label = self._get_app_label()
            template_name = f'apps/{app_label}/partials/search-results.html'
        
        return render(request, template_name , context)