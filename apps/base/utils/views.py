from abc import ABC, abstractmethod

from django.contrib import messages
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from apps.activities.models import Activity

class Deleter(ABC):
    """
    utility class to achieve delete functionality.  
    ### required methods:  
    - `can_delete_criteria()` -> bool  
    ### optional methods:
    - `get_delete_message()` -> str  
    - `get_cannot_delete_message()` -> str  
    ### optional attributes:  
    - `schema_class: ninja.ModelSchema` to use it to serialize complex data types into Activity.old_data: JSONField  
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
    
    def _add_activity(
        self, obj, old_data: dict | None = None
    ) -> None:
        
        app_label = self.instance.__class__._meta.app_label
        content_type = ContentType.objects.get(app_label=app_label)

        activity = {
            'user': self.request.user,
            'type': Activity.TypeChoices.DELETE,
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

        Klass = self.instance.__class__
        old_data = Klass.objects.values().get(id=self.instance.id)
        old_data = {
            k:v for k,v in old_data.items() 
            if k not in ['slug', 'search']
        }

        self._add_activity(
            self.instance, old_data=old_data
        )

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