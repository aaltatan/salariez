from abc import ABC, abstractmethod

from django.http import HttpResponse
from django.shortcuts import render


class AbstractList(ABC):
    
    @property
    @abstractmethod
    def resource_class(self): ...
    
    @property
    @abstractmethod
    def filter_class(self): ...
    
    @property
    @abstractmethod
    def filename(self): ...


class ExportMixin(AbstractList):
    
    def get(self, request, *args, **kwargs):
        
        if request.htmx:
            response = HttpResponse()
            response['Hx-Redirect'] = request.get_full_path()
            return response
        
        qs = self.filter_class(data=request.GET or None).qs
        
        extension = request.GET.get('extension', 'csv')
        
        data = self.resource_class().export(qs)
        
        response = HttpResponse(getattr(data, extension))
        response['Content-Disposition'] = (
            f'attachment; filename="{self.filename}.{extension}"'
        )
        return response
    
    def post(self, request, *args, **kwargs):
        
        context = {
            'path': request.get_full_path()
        }
        
        return render(request, 'partials/export-modal.html', context)