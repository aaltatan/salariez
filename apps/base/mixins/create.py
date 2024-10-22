from abc import ABC, abstractmethod

from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from . import utils

from apps.activities.models import Activity


class AbstractCreate(ABC):
    
    @property
    @abstractmethod
    def form_class(self): ...


class CreateMixin(utils.HelperMixin, AbstractCreate):
    """
    utility class to implement add new record.  
    
    ### required attributes:  
    - `form_class: ModelForm` to use it inside form_template_name
    
    ### optional attributes:  
    - `template_name: str` to use it as main template  
    - `form_template_name: str` like: `'partials/create-form.html'`
    - `index_template_name: str` like: `'apps/<app_name>/index.html'`  
    - `success_path: str` like: `'<app_name>:index'` 
    - `continue_updating: bool`  
     
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

        if request.GET.get('modal'):
            template_name = self._get_template_name_create_update_partial()
        else:
            template_name = self._get_template_name_create_update()

        return render(
            request, template_name, context
        )
    
    def delete(self, request: HttpRequest) -> HttpResponse:
        
        form_template_name = self._get_form_template_name()
        context = {'form': self.form_class()}
        
        return render(request, form_template_name, context)
    
    def _add_activity(
        self, obj, new_data: dict | None = None
    ) -> None:
        
        content_type = (
            ContentType
            .objects
            .filter(app_label=self._get_app_label())
            .first()
        )

        activity = {
            'user': self.request.user,
            'type': Activity.TypeChoices.CREATE,
            'content_type': content_type,
            'object_id': obj.id,
        }

        if new_data:
            activity['new_data'] = new_data

        Activity(**activity).save()

    def _base_post(self, request: HttpRequest) -> HttpResponse:

        form = self.form_class(request.POST, request.FILES)
        context = {'form': form}

        if form.is_valid():
            obj = form.save()
            self._add_activity(obj)
            messages.success(
                request, _('{} has been created successfully'.format(obj))
            )
            
            if request.POST.get('save'):
                if getattr(self, 'continue_updating', None) is not None and self.continue_updating:
                    return self._get_success_save_update_response(obj)
                else:
                    return self._get_success_save_update_response()
            
            if request.POST.get('save_and_add_another'):
                context = {'form': self.form_class()}
        
        form_template_name = self._get_form_template_name()
        
        response = render(request, form_template_name, context)
        response['HX-Trigger'] = 'get-messages'
        response['HX-reswap'] = 'outerHTML'

        return response

    def _modal_post(self, request):

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            self._add_activity(obj)
            messages.success(
                request, _('{} has been created successfully'.format(obj))
            )
            form = self.form_class()
            response = HttpResponse('')
            response['HX-Retarget'] = '#no-content'
            response['HX-Trigger'] = 'get-messages'
            return response

        template_name = self._get_template_name_create_update_partial()
        context = {'form': form}

        response = render(request, template_name, context)
        response['HX-Retarget'] = '#modal'
        response['HX-Trigger'] = 'get-messages'

        return response
    
    def post(self, request: HttpRequest) -> HttpResponse:
        
        if request.GET.get('modal'):
            return self._modal_post(request)
        
        return self._base_post(request)