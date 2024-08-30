from typing import Literal

from django.shortcuts import render
from django.urls import reverse


class HelperMixin:
    
    def get_success_save_update_response(self):
        """
        to use it inside create and update mixins.
        """
        response = render(self.request, self._get_index_template_name())
        response['HX-Retarget'] = '#app'
        response['HX-Reselect'] = '#app'
        response['HX-Push-Url'] = reverse(self._get_success_path())
        return response

    def get_default_ordering(self):
        """
        to use it to set default order in list mixin queryset  
        """
        model = self.get_model_class()
        return model._meta.ordering
    
    def get_model_class(self):
        """
        get model class from derived `form_class` if model does not exists
        """
        if hasattr(self, 'model'):
            return self.model
        
        model_class = self.form_class._meta.model
        return model_class
    
    def get_app_label(self):
        """
        get app label from model class
        """
        model_class = self.get_model_class()
        app_name: str = model_class._meta.app_label
        
        return app_name
    
    def get_modal_template_name(self):
        """
        get modal template name to use it in delete mixin
        """
        if hasattr(self, 'modal_template_name'):
            return self.modal_template_name
        
        return 'partials/delete-modal.html'
    
    def get_form_template_name(
        self, view: Literal['update', 'create'] = 'create'
    ):
        """to use it in create and update mixins
        Args:
            view (Literal[&#39;update&#39;, &#39;create&#39;], optional): _description_. Defaults to 'create'.
        """
        if hasattr(self, 'form_template_name'):
            return self.form_template_name
        
        return f'partials/{view}-form.html'
    
    def _get_success_path(self):
        
        if hasattr(self, 'success_path'):
            return self.success_path
        
        app_name = self.get_app_label()
        return f'{app_name}:index'
    
    def get_hx_location_path(self):
        """
        to use it in delete mixin
        """
        if hasattr(self, 'hx_location_path'):
            return self.hx_location_path
        
        app_name = self.get_app_label()
        return f'{app_name}:index'
    
    def get_hx_location_target(self):
        """
        to use it in delete mixin
        """
        if hasattr(self, 'hx_location_target'):
            return self.hx_location_target
        
        app_name = self.get_app_label()
        return f'#{app_name}-table'
    
    def _get_index_template_name(self):
        
        if hasattr(self, 'index_template_name'):
            return self.index_template_name
        
        app_name = self.get_app_label()
        
        return f'apps/{app_name}/index.html'