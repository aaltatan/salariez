from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

class PositionForm(forms.ModelForm):
    
    class Meta:
        model = models.Position
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('position name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            "description": forms.Textarea(
                attrs={
                    "x-autosize": "",
                    "rows": "1",
                    "autocomplete": "on",
                    "placeholder": _("position's description"),
                }
            ),
        }
