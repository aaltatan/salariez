from apps.base.utils import views


class Deleter(views.Deleter):
    def can_delete_criteria(self):
        return True