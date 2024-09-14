from abc import abstractmethod, ABC

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render


class AbstractTree(ABC):
    
    @property
    @abstractmethod
    def model(self):
        ...


class TreeMixin(AbstractTree):
    """
    ### required attributes:  
    - `model: Model | MPTTModel`  
    
    ### optional attributes:  
    - `template_name: str` like: `'apps/<app_name>/index.html'`
    - `body_template_name: str` like: `'apps/<app_name>/partials/body.html'`  
    """
    def _get_app_label(self) -> str:
        
        app_label = self.model._meta.app_label
        return app_label
    
    def _get_template_name(self) -> str:
        """
        you can set `template_name` attr in view class instead.  
        """
        if getattr(self, 'template_name', None) is not None:
            return self.template_name
        
        app_label = self._get_app_label()
        
        return f'apps/{app_label}/index.html'
    
    def _get_body_template_name(self) -> str:
        """
        you can set `body_template_name` attr in view class instead.  
        """
        if getattr(self, 'body_template_name', None) is not None:
            return self.body_template_name
        
        app_label = self._get_app_label()
        return f'apps/{app_label}/partials/body.html'
    
    def get(self, request, *args, **kwargs):
        
        qs = self.model.objects.all()
        context = {'qs': qs}
        
        template_name = self._get_body_template_name()
        
        if not request.htmx or request.htmx.boosted:
            template_name = self._get_template_name()
        
        return render(request, template_name, context)