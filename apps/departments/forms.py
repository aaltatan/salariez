from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import get_textarea_field
from apps.base.widgets import SearchWidget


WIDGETS = {
    "name": forms.TextInput({
        "placeholder": _("department's name"),
        "autofocus": "on",
        "autocomplete": "on",
    }),
    "department_id": forms.TextInput({
        'placeholder': _("department's id"),
        'x-mask': '999999999999',
    }),
    "description": get_textarea_field(
        placeholder=_("department's description")
    ),
    "cost_center": SearchWidget(),
    "parent": SearchWidget(),
}


class DepartmentCreateForm(forms.ModelForm):

    class Meta:
        model = models.Department
        fields = [
            'name', 
            'cost_center', 
            'parent', 
            'description'
        ]
        widgets = WIDGETS


class DepartmentUpdateForm(forms.ModelForm):

    class Meta:
        model = models.Department
        fields = [
            'name', 
            'cost_center', 
            'parent', 
            'department_id', 
            'description'
        ]
        widgets = WIDGETS

