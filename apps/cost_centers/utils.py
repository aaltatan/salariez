from apps.base.utils import views


class Deleter(views.Deleter):
    def can_delete_condition(self) -> bool:
        conditions = [
            not self.instance.departments.all().exists()
        ]
        return conditions