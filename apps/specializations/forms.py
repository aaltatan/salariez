from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import get_textarea_field


class SpecializationForm(forms.ModelForm):
    
    class Meta:
        model = models.Specialization
        fields = ['name', 'is_specialist', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('specialization name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            'is_specialist': forms.Select(
                choices=models.IS_SPECIALIST_CHOICES
            ),
            "description": get_textarea_field(
                placeholder=_("specialization's description")
            ),
        }
