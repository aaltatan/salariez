from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy

from . import models


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = models.Department
        exclude = ["slug"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": _("department's name"),
                    "autofocus": "on",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "x-autosize": "",
                    "rows": "1",
                    "placeholder": _("department's description"),
                }
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        hx_get_path = reverse_lazy("departments:search")
        parent = self.initial.get("parent")
        
        parent = self.data.get('parent', parent)
        
        if parent:
            hx_get_path = (
                f'{reverse("departments:search")}?id={parent}&name=parent'
            )

        self.fields["parent"].widget = forms.TextInput(
            attrs={
                "hx-get": hx_get_path ,
                "hx-trigger": "load",
                "hx-target": "this",
            }
        )
