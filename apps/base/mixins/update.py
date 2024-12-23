from abc import ABC, abstractmethod

from django.urls import reverse
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
    - `template_name: str` like `apps/<app_name>/update.html`
    - `form_template_name: str` like: `'partials/create-form.html'`
    - `index_template_name: str` like: `'apps/<app_name>/index.html'`  
    - `success_path: str` like: `'<app_name>:index'` 
     
    also you need to implement `get_create_path` property in the model which the `form_class` inherit from.
    """
    
    def get(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:

        instance = get_object_or_404(self._get_model_class(), slug=slug)
        template_name = self._get_template_name_create_update('update')
        context = self.get_context_data(instance)

        return render(request, template_name, context)
    
    # handle reset button
    def delete(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:

        instance = get_object_or_404(self._get_model_class(), slug=slug)
        context = self.get_context_data(instance)
        form_template_name = self._get_form_template_name('update')
        
        return render(request, form_template_name, context)
    
    def get_context_data(self, instance):
        return {
            'form': self.form_class(instance=instance),
            'instance': instance,
            'can_delete': self._has_perm('delete'),
            'breadcrumbs': self._get_breadcrumbs(instance),
        }
    
    def _get_breadcrumbs(self, instance) -> list:
        if getattr(self, 'breadcrumbs', None):
            return self.breadcrumbs
        
        app_label = self._get_app_label()

        return [
            {
                'text': _('Home'),
                'href': reverse('base:index'),
                'active': False,
            },
            {
                'text': self._get_model_class()._meta.verbose_name_plural,
                'href': reverse(f'{app_label}:index'),
                'active': False,
            },
            {
                'text': _('Update {}').format(instance),
                'href': reverse(f'{app_label}:update', args=[instance.slug]),
                'active': True,
            },
        ]
    
    def _add_activity(
        self, obj, old_data: dict | None = None,
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
            activity['old_data'] = old_data

        Activity(**activity).save()

    def _delete_handler(self, request: HttpRequest, instance) -> HttpResponse:
        perms = (
            request
            .user
            .user_permissions
            .filter(codename__startswith="delete_")
        )

        can_delete_models = [
            p.content_type.model_class() for p in perms
        ]

        model = self._get_model_class()

        if model in can_delete_models or request.user.is_superuser:
            self.deleter(instance, request).delete()
        else:
            messages.error(
                request, 
                _('you can\'t delete this ({}) because you don\'t have permission to do so').format(instance)
            )
        return self._get_success_save_update_response() 

    def post(
        self, request: HttpRequest, slug: str, *args, **kwargs
    ) -> HttpResponse:
        
        instance = get_object_or_404(self._get_model_class(), slug=slug)
        
        form = self.form_class(
            request.POST, request.FILES, instance=instance
        )
        
        if request.POST.get('delete'):
            return self._delete_handler(request, instance)
        
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