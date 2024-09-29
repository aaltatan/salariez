from django import forms

from . import models
from apps.base.utils.fields import get_date_field


class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model = models.Employee
        fields = '__all__'
        widgets = {
            'birth_date': get_date_field(),
            'card_date': get_date_field(required=False),
            'hire_date': get_date_field(),
        }