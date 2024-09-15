from abc import ABC, abstractmethod

from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from mptt.exceptions import InvalidMove

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
    
    ### required attributes:  
    - `template_name: str` like `apps/<app_name>/update.html`
    - `form_class: ModelForm`
    
    ### optional attributes:  
    - `form_template_name: str` like: `'partials/create-form.html'`
    - `index_template_name: str` like: `'apps/<app_name>/index.html'`  
    - `success_path: str` like: `'<app_name>:index'` 
     
    also you need to implement `get_create_path` property in the model which the `form_class` inherit from.
    """
    
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        
        instance = get_object_or_404(self._get_model_class(), slug=slug)
        
        context = {
            'form': self.form_class(instance=instance),
            'instance': instance
        }
        return render(request, self.template_name, context)
    
    def delete(self, request: HttpRequest, slug: int) -> HttpResponse:
        
        instance = get_object_or_404(self._get_model_class(), slug=slug)
        
        context = {
            'form': self.form_class(instance=instance),
            'instance': instance
        }
        
        form_template_name = self._get_form_template_name('update')
        
        return render(request, form_template_name, context)
    
    def post(
        self, request: HttpRequest, slug: int, *args, **kwargs
    ) -> HttpResponse:
            
        instance = get_object_or_404(self._get_model_class(), slug=slug)
        
        form = self.form_class(data=request.POST, instance=instance)
        
        if request.POST.get('delete'):
            
            kwargs['slug'] = slug
            
            if self.cannot_delete(request, *args, **kwargs) is None:
                instance.delete()
                messages.success(
                    request,
                    _(
                        '{} has been deleted successfully'
                        .format(instance)
                    )
                )
            return self._get_success_save_update_response() 
        
        if form.is_valid():
            try:
                obj = form.save()
                messages.success(
                    request, 
                    _('{} has been updated successfully'.format(obj))
                )
                if request.POST.get('update'):
                    return self._get_success_save_update_response()
            except InvalidMove as error:
                form.add_error('parent', error)

        form_template_name = self._get_form_template_name('update')
        context = {'form': form, 'instance': instance}
        
        return render(request, form_template_name, context)