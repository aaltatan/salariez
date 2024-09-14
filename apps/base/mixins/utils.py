from typing import Literal

from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm


class HelperMixin:
    
    def _get_success_save_update_response(self):
        """
        to use it inside create and update mixins.
        """
        response = render(self.request, self._get_index_template_name())
        response['HX-Retarget'] = '#app'
        response['HX-Reselect'] = '#app'
        response['HX-Push-Url'] = reverse(self._get_success_path())
        return response

    def _get_default_ordering(self):
        """
        to use it to set default order in list mixin queryset  
        """
        model = self._get_model_class()
        return model._meta.ordering
    
    def _get_model_class(self):
        """
        get model class from derived `form_class` if model does not exists
        """
        if hasattr(self, 'model'):
            return self.model
        
        form_class: ModelForm = self.form_class
        model_class = form_class._meta.model
        return model_class
    
    def _get_app_label(self):
        """
        get app label from model class
        """
        model_class = self._get_model_class()
        app_label: str = model_class._meta.app_label
        
        return app_label
    
    def _get_modal_template_name(self):
        """
        you can set `modal_template_name` in view class instead.  
        """
        if hasattr(self, 'modal_template_name'):
            return self.modal_template_name
        
        return 'partials/delete-modal.html'
    
    def _get_form_template_name(
        self, view: Literal['update', 'create'] = 'create'
    ):
        """
        you can set `form_template_name` in view class instead.  
        """
        if hasattr(self, 'form_template_name'):
            return self.form_template_name
        
        return f'partials/{view}-form.html'
    
    def _get_success_path(self):
        """
        you can set `success_path` in view class instead.  
        """
        if hasattr(self, 'success_path'):
            return self.success_path
        
        app_name = self._get_app_label()
        return f'{app_name}:index'
    
    def _get_hx_location_path(self):
        """
        you can set `hx_location_path` in view class instead.  
        """
        if hasattr(self, 'hx_location_path'):
            return self.hx_location_path
        
        app_name = self._get_app_label()
        return f'{app_name}:index'
    
    def _get_hx_location_target(self):
        """
        you can set `hx_location_target` in view class instead.  
        """
        if hasattr(self, 'hx_location_target'):
            return self.hx_location_target
        
        app_name = self._get_app_label()
        return f'#{app_name}-table'
    
    def _get_index_template_name(self):
        """
        you can set `index_template_name` in view class instead.  
        """
        if hasattr(self, 'index_template_name'):
            return self.index_template_name
        
        app_name = self._get_app_label()
        
        return f'apps/{app_name}/index.html'