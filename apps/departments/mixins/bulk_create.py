from abc import abstractmethod, ABC

from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from .. import utils


class AbstractBulkCreate(ABC):
    
    @property
    @abstractmethod
    def model(self):
        ...


class BulkCreateMixin(AbstractBulkCreate):
    
    def get(self, request, *args, **kwargs):
        
        utils.create_faculties(self.model)
        messages.success(
            request, _('departments has been created successfully')
        )
        response = HttpResponse('')
        response['Hx-Retarget'] = '#no-content'
        response['Hx-Reswap'] = 'innerHTML'
        return response