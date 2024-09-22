from abc import ABC, abstractmethod

from django.http import HttpResponse
from django.shortcuts import render


class AbstractExport(ABC):
    
    @property
    @abstractmethod
    def resource_class(self): ...


class ExportMixin(AbstractExport):
    """
    utility mixin to achieve export functionality.  
    
    ### required attributes:  
    - `resource_class: ModelResource`  
    
    ### optional attributes:  
    - `filename: str`
    - `filter_class: FilterSet`
    """
    
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
        
        qs = self._get_queryset()
        
        dataset = self.resource_class().export(qs)
        
        response = HttpResponse(
            getattr(dataset, extension),
            content_type=content_types[extension]
        )
        response['Content-Disposition'] = (
            f'attachment; filename="{self._get_filename()}.{extension}"'
        )
        return response
    
    def post(self, request, *args, **kwargs):
        
        context = {
            'path': request.get_full_path()
        }
        
        return render(request, 'partials/modals/export.html', context)
    
    def _get_filename(self):
        
        app_label = self._get_model_class()._meta.app_label
        filename = getattr(self, 'filename', app_label)
        
        if filename == '':
            return app_label
        
        return filename
    
    def _get_model_class(self):
        
        Klass = self.resource_class._meta.model
        
        return Klass
    
    def _get_queryset(self):
        
        Klass = self._get_model_class()
        
        qs = Klass.objects.all()
        
        if getattr(self, 'filter_class', None):
            qs = self.filter_class(data=self.request.GET or None).qs
        
        return qs