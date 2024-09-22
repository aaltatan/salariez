from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from . import models

from apps.cost_centers import models as cc_models
from apps.base.utils import get_search_input, Object


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
    "description": forms.Textarea({
        "x-autosize": "",
        "rows": "1",
        "autocomplete": "on",
        "placeholder": _("department's description"),
    }),
}

class InitializerMixin:

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # departments search field
        parent = Object(
            url_name='departments:search', 
            field_name='parent', 
            model=models.Department,
            value_attributes=['department_id', 'name'],
        )
        self.fields['parent'].widget = get_search_input(
            widget=widgets.TextInput,
            form=self, 
            obj=parent
        )

        # cost centers search field
        cost_center = Object(
            url_name='cost_centers:search', 
            field_name='cost_center', 
            model=cc_models.CostCenter,
            value_attributes=['name'],
            required=True,
            is_modal=True,
            add_new_url=('cost_centers:create', 'cost_centers.add_costcenter')
        )
        self.fields['cost_center'].widget = get_search_input(
            widget=widgets.TextInput,
            form=self, 
            obj=cost_center,
        )


class DepartmentCreateForm(InitializerMixin, forms.ModelForm):

    class Meta:
        model = models.Department
        fields = [
            'name', 
            'cost_center', 
            'parent', 
            'description'
        ]
        widgets = WIDGETS


class DepartmentUpdateForm(InitializerMixin, forms.ModelForm):

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

