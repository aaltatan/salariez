from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import get_textarea_field


class PositionForm(forms.ModelForm):
    
    class Meta:
        model = models.Position
        fields = ['name', 'order', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('position name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            "description": get_textarea_field(
                placeholder=_("position's description")
            ),
        }
