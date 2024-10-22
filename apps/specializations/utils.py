from apps.base.utils import views


class Deleter(views.Deleter):
    def can_delete_condition(self):
        conditions = [
            not self.instance.education_transactions.all().exists()
        ]
        return all(conditions)