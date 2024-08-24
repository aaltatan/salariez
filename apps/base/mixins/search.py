from abc import ABC, abstractmethod

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse


class AbstractSearch(ABC):
    
    @property
    @abstractmethod
    def input_placeholder(self): ...
    
    @property
    @abstractmethod
    def model(self): ...


class SearchMixin:
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        placeholder = request.GET.get('placeholder')
        if placeholder is None:
            placeholder = self.input_placeholder
        
        context = {
            'path': reverse('faculties:search'),
            'placeholder': placeholder
        } 
        
        return render(request, 'components/inputs/search.html', context)
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        q = request.POST.get('q', '')
        context = {}
        
        if q is None or q == '':
            context['qs'] = self.model.objects.none()
        else:
            context['qs'] = self.model.objects.filter(search__contains=q)
        
        return render(request, 'apps/faculties/partials/search-results.html', context)