from django.utils.translation import gettext as _

from apps.base.utils import views


class Deleter(views.Deleter):
    def can_delete_condition(self) -> bool:
        conditions = [
            not self.instance.currency.is_local,
        ]
        return all(conditions)
    
    def get_cannot_delete_message(self):
        return _('you can\'t delete this exchange rate transaction because either is for local currency or related to another models in the system')