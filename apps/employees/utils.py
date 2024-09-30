from . import schemas

from apps.base.utils import views


class Deleter(views.Deleter):

    schema_class = schemas.EmployeeSchema

    def can_delete_criteria(self) -> bool:
        return True