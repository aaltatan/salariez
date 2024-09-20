from abc import ABC, abstractmethod

from django.contrib import messages
from django.http import HttpRequest
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
    def __init__(
        self, 
        instance, 
        request: HttpRequest,
        send_delete_messages: bool = True,
        send_cannot_delete_messages: bool = True,
    ) -> None:
        self.instance = instance
        self.request = request
        self.send_delete_messages = send_delete_messages
        self.send_cannot_delete_messages = send_cannot_delete_messages

    def get_delete_message(self):
        return _('{} has been deleted successfully').format(self.instance)
    
    def get_cannot_delete_message(self):
        return _('you can\'t delete this ({}) because there is one or more models related to it.').format(self.instance)

    def failure_scenario(self) -> None:
        if self.send_cannot_delete_messages:
            messages.error(
                self.request, self.get_cannot_delete_message()
            )

    def success_scenario(self) -> None:
        self.instance.delete()
        if self.send_delete_messages:
            messages.success(
                self.request, self.get_delete_message()
            )

    @abstractmethod
    def can_delete_criteria(self) -> bool:
        ...

    def delete(self) -> None:
        
        can_be_deleted = self.can_delete_criteria()
        
        if can_be_deleted:
            self.success_scenario()
        else:
            self.failure_scenario()