from django.utils.translation import gettext_lazy as _
from django.conf import settings

from braces.views._access import AccessMixin


class DebugRequiredMixin(AccessMixin):
    
    def dispatch(self, request, *args, **kwargs):
        if settings.DEBUG is False:
            return self.handle_no_permission(request)

        return super().dispatch(
            request, *args, **kwargs
        )