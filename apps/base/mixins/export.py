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
    


class ExportMixin(AbstractList):
    
    def get(self, request, *args, **kwargs):
        
        if request.htmx:
            response = HttpResponse()
            response['Hx-Redirect'] = request.get_full_path()
            return response
        
        content_types = {
            'csv': 'text/csv',
            'json': 'application/json',
            'xlsx': 'application/vnd.ms-excel',
        }
        allowed_extensions = list(content_types.keys())
        extension = request.GET.get('extension', 'csv').lower()
        
        if extension not in allowed_extensions:
            extension = 'xlsx'
            
        qs = self.filter_class(data=request.GET or None).qs
        
        dataset = self.resource_class().export(qs)
        
        response = HttpResponse(
            getattr(dataset, extension),
            content_type=content_types[extension]
        )
        response['Content-Disposition'] = (
            f'attachment; filename="{self.get_filename()}.{extension}"'
        )
        return response
    
    def post(self, request, *args, **kwargs):
        
        context = {
            'path': request.get_full_path()
        }
        
        return render(request, 'partials/export-modal.html', context)
    
    def get_filename(self):
        
        app_label = self.filter_class._meta.model._meta.app_label
        filename = getattr(self, 'filename', app_label)
        
        if filename == '':
            return app_label
        
        return filename
        