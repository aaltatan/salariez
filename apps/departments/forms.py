from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.cost_centers import models as cc_models
from apps.base.utils import get_search_input


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = models.Department
        fields = [
            'name', 
            'cost_center', 
            'parent', 
            'department_id', 
            'description'
        ]
        widgets = {
            "name": forms.TextInput({
                "placeholder": _("department's name"),
                "autofocus": "on",
                "autocomplete": "on",
            }),
            "department_id": forms.TextInput({
                'placeholder': _("department's id"),
                'x-mask': '999999999999',
            }),
            "description": forms.Textarea({
                "x-autosize": "",
                "rows": "1",
                "autocomplete": "on",
                "placeholder": _("department's description"),
            }),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # departments search field
        self.fields['parent'].widget = get_search_input(
            form=self, 
            url_name='departments:search', 
            field_name='parent', 
            model=models.Department,
            value_attributes=['department_id', 'name'],
        )

        # cost centers search field
        self.fields['cost_center'].widget = get_search_input(
            form=self, 
            url_name='cost_centers:search', 
            field_name='cost_center', 
            model=cc_models.CostCenter,
            value_attributes=['name'],
        )