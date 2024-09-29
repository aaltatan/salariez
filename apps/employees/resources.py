
from import_export import resources

from . import models


class EmployeeRecourse(resources.ModelResource):

    class Meta:
        model = models.Employee
        fields = ["firstname"]
    
    # def dehydrate_name(self, obj):