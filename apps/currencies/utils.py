from apps.base.utils import views


class Deleter(views.Deleter):
    def can_delete_condition(self) -> bool:
        conditions = [
            not self.instance.is_local,
        ]
        return all(conditions)