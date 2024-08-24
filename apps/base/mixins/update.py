from abc import ABC, abstractmethod

from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from . import utils


class AbstractUpdate(ABC):
    
    @property
    @abstractmethod
    def template_name(self):
        ...
    
    @property
    @abstractmethod
    def form_class(self):
        ...


class UpdateMixin(utils.HelperMixin, AbstractUpdate):
    
    """
    utility class for implement update record functionality.  
    you need to set those attributes on derived class:  
    - `template_name: str` like `apps/<app_name>/update.html`
    - `form_class: ModelForm`
    """
    
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        
        instance = get_object_or_404(self.get_model_class(), slug=slug)
        
        context = {
            'form': self.form_class(instance=instance),
            'instance': instance
        }
        return render(request, self.template_name, context)
    
    def delete(self, request: HttpRequest, slug: int) -> HttpResponse:
        
        instance = get_object_or_404(self.get_model_class(), slug=slug)
        
        context = {
            'form': self.form_class(instance=instance),
            'instance': instance
        }
        
        form_template_name = self.get_form_template_name('update')
        
        return render(request, form_template_name, context)
    
    def post(self, request: HttpRequest, slug: int) -> HttpResponse:
            
        instance = get_object_or_404(self.get_model_class(), slug=slug)
        
        form = self.form_class(data=request.POST, instance=instance)
        context = {'form': form, 'instance': instance}
        
        if form.is_valid():
            
            form.save()
            messages.info(request, _('done'), 'bg-green-600')
            
            if request.POST.get('update'):
                return self.get_success_save_update_response()
            
        form_template_name = self.get_form_template_name('update')
            
        return render(request, form_template_name, context)