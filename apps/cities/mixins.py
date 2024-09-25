from django.utils.translation import gettext_lazy as _

from .utils import Deleter

from apps.base.mixins.bulk import BulkActionMixin


class BulkDeleteMixin(BulkActionMixin):

    bulk_content_template_path = 'partials/bulk-contents/delete.html'
    bulk_path = 'cities:bulk-delete'
    deleter = Deleter

    def modal_action(self, pks: list[int], request):
        
        qs = self.model.objects.filter(pk__in=pks)

        for instance in qs:
            self.deleter(instance, request).delete()
        
        return 