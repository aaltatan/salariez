from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

class CityForm(forms.ModelForm):
    
    class Meta:
        model = models.City
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('city name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            "description": forms.Textarea(
                attrs={
                    "x-autosize": "",
                    "rows": "1",
                    "autocomplete": "on",
                    "placeholder": _("city's description"),
                }
            ),
        }