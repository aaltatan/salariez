from abc import ABC, abstractmethod

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.urls import reverse

from .. import utils


class AbstractBulkAction(ABC):
    
    @abstractmethod
    def modal_action(self): ...
    
    @property
    @abstractmethod
    def bulk_path(self): ...


class BulkActionMixin(utils.HelperMixin, AbstractBulkAction):
    """
    ### required methods:  
    - `modal_action`: to implement the bulk action logic  
    ### required attributes:  
    - `bulk_content_template_path` **OR** `bulk_content_template_name`
    - `bulk_path : str` like: `'<app_name>:bulk-delete'` 
    """
    def get_bulk_path(self):
        return reverse(self.bulk_path)
    
    def get_bulk_contents_template(self):
        """
        like `'apps/<app_label>/partials/bulk-contents/<bulk_content_template_name>.html'`
        """
        path_criteria = (
            getattr(self, 'bulk_content_template_path', None) is not None
        )
        if path_criteria:
            return self.bulk_content_template_path
        
        name_criteria = (
            getattr(self, 'bulk_content_template_name', None) is not None
        )

        if name_criteria:
            app_label = self._get_app_label()
            template_name = self.bulk_content_template_name

            return (
                f'apps/{app_label}/partials/bulk-contents/{template_name}.html'
            )
        
        raise NotImplementedError(
            'you must set either bulk_content_template_name or bulk_content_template_path attributes in this derived mixin'
        )
    
    def get_queryset(self):

        pks = self.get_get_pks()
        return self.model.objects.filter(pk__in=pks)

    def get_context_data(self):

        return {'qs': self.get_queryset()}

    def get_modal_content(self):
        
        context = self.get_context_data()
        template_name = self.get_bulk_contents_template()
        return render_to_string(template_name, context, self.request)