from abc import abstractmethod, ABC

from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from .. import utils


class AbstractEmpty(ABC):
    
    @property
    @abstractmethod
    def model(self):
        ...


class EmptyMixin(AbstractEmpty):
    
    def get(self, request, *args, **kwargs):
        
        utils.empty_departments(self.model)
        messages.success(
            request, _('departments has been deleted successfully')
        )
        response = HttpResponse('')
        response['Hx-Retarget'] = '#no-content'
        response['Hx-Reswap'] = 'innerHTML'
        return response