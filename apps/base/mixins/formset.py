from abc import ABC, abstractmethod

from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.contrib import messages
from django.http import HttpResponse


class FormsetMixinAbstract(ABC):
    
    @property
    @abstractmethod
    def parent_model(self): ...
    
    @property
    @abstractmethod
    def form_class(self): ...

    @abstractmethod
    def post_save(self, instance): ...
    


class FormSetMixin(FormsetMixinAbstract):
    """
    utility class for implement update employee related models from employee application itself.  
    ### required attributes:  
    - `parent_model: Model`
    - `form_class: ModelForm`
    ### required methods:  
    - `post_save: Callable`: to perform an action after formset has been saved.  
    ### optional attributes:  
    - `model: Model`  
    - `template_name: str`  
    - `partial_template_name: str`  
    """
    def get(self, request, slug: str, *args, **kwargs):

        context = self.get_context_data(slug)
        template_name = self.get_template_name()

        return self.get_response(template_name, context)
    
    def post(self, request, slug: str, *args, **kwargs):

        context = self.get_context_data(slug)
        template_name = self.get_partial_template_name()

        return self.get_response(template_name, context)
    
    def get_context_data(self, slug: str) -> dict:

        instance = get_object_or_404(self.parent_model, slug=slug)

        Formset = self.get_formset_class()
        formset = Formset(
            self.request.POST or None, instance=instance
        )

        if formset.is_valid():
            formset.save()
            self.post_save(instance=instance)
            messages.success(self.request, _('done'))
            formset = Formset(instance=instance)

        return {'instance': instance, 'formset': formset}

    def get_response(self, template_name, context) -> HttpResponse:
        
        response = render(self.request, template_name, context)
        response['HX-Trigger'] = 'get-messages'
        return response

    def get_model_class(self):

        if getattr(self, 'model', None) is not None:
            return self.model
        
        return self.form_class._meta.model

    def get_app_label(self) -> str:
        return self.get_model_class()._meta.verbose_name_plural.replace(' ', '-')

    def get_parent_app_label(self) -> str:
        return self.parent_model._meta.app_label

    def get_template_name(self) -> str:

        if getattr(self, 'template_name', None) is not None:
            return self.template_name
        
        parent_app_label = self.get_parent_app_label()
        app_label = self.get_app_label()
        
        return f'apps/{parent_app_label}/formsets/{app_label}.html'

    def get_partial_template_name(self) -> str:

        if getattr(self, 'partial_template_name', None) is not None:
            return self.partial_template_name
        
        parent_app_label = self.get_parent_app_label()
        app_label = self.get_app_label()
        
        return f'apps/{parent_app_label}/partials/formsets/{app_label}.html'
    
    def get_formset_class(self):

        return inlineformset_factory(
            parent_model=self.parent_model,
            model=self.get_model_class(),
            form=self.form_class,
            can_delete=True,
            extra=1,
        )