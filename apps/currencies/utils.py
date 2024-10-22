from django.utils.translation import gettext as _

from apps.base.utils import views


class Deleter(views.Deleter):
    def can_delete_condition(self) -> bool:
        conditions = [
            not self.instance.is_local,
            not self.instance.rates.all().exists()
        ]
        return all(conditions)
    
    def get_cannot_delete_message(self):
        return _('you can\'t delete {} because either it related to another model or is local currency').format(self.instance)