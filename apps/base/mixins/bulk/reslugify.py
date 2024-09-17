from abc import ABC, abstractmethod

from .action import BulkActionMixin
from ...admin_actions import reslugify_action


class ReslugifyAbstract(ABC):
    
    @property
    @abstractmethod
    def model(self):
        ...


class ReslugifyModalMixin(BulkActionMixin, ReslugifyAbstract):

    bulk_content_template_path = 'partials/bulk-contents/reslugify.html'

    def modal_action(self, pks: list[int]):
        qs = self.model.objects.filter(pk__in=pks)
        reslugify_action(self.request, qs)