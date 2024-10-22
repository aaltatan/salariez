import json
from typing import Literal

from django.urls import reverse
from django.http import HttpResponse


class HelperMixin:

    @staticmethod
    def _app_label_to_spaces(app_label: str):
        if '_' in app_label:
            return app_label.replace(' ', '-')
        return app_label

    @staticmethod
    def _app_label_to_kebab(app_label: str):
        if '_' in app_label:
            return app_label.replace('_', '-')
        return app_label
    
    def _get_success_save_update_response(self, obj = None):
        """
        to use it inside create and update mixins.
        """
        hx_location = {
            'target': '#app',
            'select': '#app',
        }
        hx_location['path'] = reverse(self._get_success_path())

        if obj is not None:
            hx_location['path'] = obj.get_update_path

        response = HttpResponse('')
        response['HX-Location'] = json.dumps(hx_location)
        response['HX-Trigger'] = 'get-messages'
        
        return response

    def _get_instance_kwargs(self, **kwargs):

        slug = kwargs.get('slug')

        if slug:
            instance_kwargs = {'slug': slug}
        else:
            instance_kwargs = {'pk': kwargs.get('pk')}

        return instance_kwargs
    
    def _get_model_class(self):
        """
        get model class from derived `form_class` if model does not exists
        """
        if getattr(self, 'model', None):
            return self.model
        
        if getattr(self, 'form_class', None):
            return self.form_class._meta.model
        
        if getattr(self, 'filter_class', None):
            return self.filter_class._meta.model
        
        raise NotImplementedError(
            'you need to set one of model, form_class or filter_class at least.'
        )
    
    def _get_app_label(self):
        """
        get app label from model class
        """
        model_class = self._get_model_class()
        app_label: str = model_class._meta.app_label
        
        return app_label
    
    def _get_object_name(self):
        """
        get app label from model class
        """
        model_class = self._get_model_class()
        object_name: str = model_class._meta.object_name
        
        return object_name.lower()
    
    def _get_modal_template_name(self):
        """
        you can set `modal_template_name` in view class instead.  
        """
        if hasattr(self, 'modal_template_name'):
            return self.modal_template_name
        
        return 'partials/modals/delete.html'
    
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
        
        app_label = self._get_app_label()
        return f'{app_label}:index'
    
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
        returns app_label in kebab case  
        you can set `hx_location_target` in view class instead.  
        """
        if hasattr(self, 'hx_location_target'):
            return self.hx_location_target
        
        app_label = self._app_label_to_kebab(self._get_app_label())
        return f'#{app_label}-table'
    
    def _get_template_name_create_update(
        self, view: Literal['update', 'create'] = 'create'
    ):
        """
        you can set `template_name` in view class instead.  
        """
        if getattr(self, 'template_name', None) is not None:
            return self.template_name
        
        app_label = self._get_app_label()
        return f'apps/{app_label}/{view}.html'
    
    def _get_template_name_create_update_partial(
        self, view: Literal['update', 'create'] = 'create'
    ):
        """
        you can set `partial_template_name` in view class instead.  
        """
        if getattr(self, 'partial_template_name', None) is not None:
            return self.partial_template_name
        
        return f'partials/modals/{view}-form.html'
    
    def _get_index_template_name(self):
        """
        you can set `index_template_name` in view class instead.  
        """
        if hasattr(self, 'index_template_name'):
            return self.index_template_name
        
        app_name = self._get_app_label()
        
        return f'apps/{app_name}/index.html'