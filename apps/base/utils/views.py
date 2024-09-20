from abc import ABC, abstractmethod

from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class Deleter(ABC):
    """
    utility class to achieve delete functionality.  
    ### required methods:  
    - `can_delete_criteria()` -> bool  
    ### optional methods:
    - `get_delete_message()` -> str  
    - `get_cannot_delete_message()` -> str  
    """
    def __init__(self, instance, request) -> None:
        self.request = request
        self.instance = instance

    def get_delete_message(self):
        return _('{} has been deleted successfully').format(self.instance)
    
    def get_cannot_delete_message(self):
        return _('you can\'t delete this ({}) because there is one or more models related to it.').format(self.instance)

    def failure_scenario(self) -> None:
        messages.error(self.request, self.get_cannot_delete_message())

    def success_scenario(self) -> None:
        self.instance.delete()
        messages.success(self.request, self.get_delete_message())

    @abstractmethod
    def can_delete_criteria(self):
        ...

    def delete(self) -> None:
        
        can_be_deleted = self.can_delete_criteria()
        
        if can_be_deleted:
            self.success_scenario()
        else:
            self.failure_scenario()