from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import get_textarea_field


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
            "description": get_textarea_field(
                placeholder=_("city's description")
            ),
        }