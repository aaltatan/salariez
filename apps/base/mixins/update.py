from abc import ABC, abstractmethod

from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType

from mptt.exceptions import InvalidMove

from . import utils

from apps.activities.models import Activity


class AbstractUpdate(ABC):
    
    @property
    @abstractmethod
    def form_class(self):
        ...
    
    @property
    @abstractmethod
    def deleter(self):
        ...


class UpdateMixin(utils.HelperMixin, AbstractUpdate):
    
    """
    utility class for implement update record functionality.  
    
    ### required attributes:  
    - `form_class: ModelForm`
    - `deleter: Deleter`
    
    ### optional attributes:  
    - `schema_class: ninja.ModelSchema` to use it to serialize complex data types into Activity.old_data: JSONField  
    - `template_name: str` like `apps/<app_name>/update.html`
    - `form_template_name: str` like: `'partials/create-form.html'`
    - `index_template_name: str` like: `'apps/<app_name>/index.html'`  
    - `success_path: str` like: `'<app_name>:index'` 
     
    also you need to implement `get_create_path` property in the model which the `form_class` inherit from.
    """
    
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        
        instance = get_object_or_404(self._get_model_class(), slug=slug)
        template_name = self._get_template_name_create_update('update')
        context = {
            'form': self.form_class(instance=instance),
            'instance': instance
        }

        return render(request, template_name, context)
    
    def delete(self, request: HttpRequest, slug: int) -> HttpResponse:
        
        instance = get_object_or_404(self._get_model_class(), slug=slug)
        
        context = {
            'form': self.form_class(instance=instance),
            'instance': instance
        }
        
        form_template_name = self._get_form_template_name('update')
        
        return render(request, form_template_name, context)
    
    def _add_activity(
        self, 
        obj, 
        old_data: dict | None = None,
    ) -> None:
        
        content_type = (
            ContentType
            .objects
            .filter(app_label=self._get_app_label())
            .first()
        )

        activity = {
            'user': self.request.user,
            'type': Activity.TypeChoices.UPDATE,
            'content_type': content_type,
            'object_id': obj.id,
        }

        if old_data:
            if hasattr(self, 'schema_class'):
                schema = self.schema_class(**old_data)
                activity['old_data'] = schema.model_dump()
            else:
                activity['old_data'] = old_data

        Activity(**activity).save()

    def post(
        self, request: HttpRequest, slug: int, *args, **kwargs
    ) -> HttpResponse:
            
        instance = get_object_or_404(self._get_model_class(), slug=slug)
        
        form = self.form_class(
            request.POST, request.FILES, instance=instance
        )
        
        if request.POST.get('delete'):
            self.deleter(instance, request).delete()
            return self._get_success_save_update_response() 
        
        if form.is_valid():
            try:
                old_data = (
                    self
                    ._get_model_class()
                    .objects
                    .values()
                    .get(id=instance.id)
                )
                self._add_activity(
                    instance, 
                    old_data=old_data,
                )
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