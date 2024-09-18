from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

class AreaForm(forms.ModelForm):
    
    class Meta:
        model = models.Area
        fields = ['name', 'city', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('area name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            "description": forms.Textarea(
                attrs={
                    "x-autosize": "",
                    "rows": "1",
                    "autocomplete": "on",
                    "placeholder": _("area's description"),
                }
            ),
        }
