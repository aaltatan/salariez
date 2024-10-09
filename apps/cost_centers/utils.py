from apps.base.utils import views


class Deleter(views.Deleter):
    def can_delete_condition(self) -> bool:
        return not self.instance.departments.all().exists()