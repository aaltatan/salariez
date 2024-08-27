from abc import ABC, abstractmethod

from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import render

from . import utils


class AbstractCreate(ABC):
    
    @property
    @abstractmethod
    def form_class(self): ...
    
    @property
    @abstractmethod
    def template_name(self): ...


class CreateMixin(utils.HelperMixin, AbstractCreate):
    
    """
    utility class to implement add new record.  
    you need to set those attributes on derived class:  
    - `form_class: ModelForm` to use it inside form_template_name
    - `form_template_name: str` to use it as partial form template
    - `template_name: str` to use it as main template  
    also you need to implement `get_create_path` property in the model which the `form_class` inherit from.
    """
    
    def get(self, request: HttpRequest) -> HttpResponse:
        
        model_class = self.form_class._meta.model
        model_name = model_class._meta.model_name
        
        if not hasattr(model_class, 'get_create_path'):
            raise NotImplementedError(f'you need to implement get_create_path property in {model_name} model')
        
        context = {'form': self.form_class(), 'instance': model_class}
        return render(request, self.template_name, context)
    
    def delete(self, request: HttpRequest) -> HttpResponse:
        
        form_template_name = self.get_form_template_name()
        context = {'form': self.form_class()}
        
        return render(request, form_template_name, context)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        
        form = self.form_class(request.POST)
        context = {'form': form}
        
        if form.is_valid():
            form.save()
            messages.success(request, _('done'))
            
            if request.POST.get('save'):
                return self.get_success_save_update_response()
            
            if request.POST.get('save_and_add_another'):
                context = {'form': self.form_class()}
        
        form_template_name = self.get_form_template_name()
        
        return render(request, form_template_name, context)