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
    
    ### required attributes:  
    - `form_class: ModelForm` to use it inside form_template_name
    - `template_name: str` to use it as main template  
    
    ### optional attributes:  
    - `form_template_name: str` like: `'partials/create-form.html'`
    - `index_template_name: str` like: `'apps/<app_name>/index.html'`  
    - `success_path: str` like: `'<app_name>:index'` 
     
    also you need to implement `get_create_path` property in the model which the `form_class` inherit from.
    """
    
    def get(self, request: HttpRequest) -> HttpResponse:
        
        model_class = self.form_class._meta.model
        model_name = model_class._meta.model_name
        
        if not hasattr(model_class, 'get_create_path'):
            raise NotImplementedError(
                f'you need to implement get_create_path property in {model_name} model'
            )
        
        context = {'form': self.form_class(), 'instance': model_class}
        return render(request, self.template_name, context)
    
    def delete(self, request: HttpRequest) -> HttpResponse:
        
        form_template_name = self._get_form_template_name()
        context = {'form': self.form_class()}
        
        return render(request, form_template_name, context)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        
        form = self.form_class(request.POST)
        context = {'form': form}
        
        if form.is_valid():
            obj = form.save()
            messages.success(request, _('{} has been created successfully'.format(obj)))
            
            if request.POST.get('save'):
                return self._get_success_save_update_response()
            
            if request.POST.get('save_and_add_another'):
                context = {'form': self.form_class()}
        
        form_template_name = self._get_form_template_name()
        
        response = render(request, form_template_name, context)
        response['HX-Trigger'] = 'get-messages'

        return response