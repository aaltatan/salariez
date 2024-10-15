from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import get_textarea_field


class EducationalDegreeForm(forms.ModelForm):
    
    class Meta:
        model = models.EducationalDegree
        fields = ['name', 'is_academic', 'order', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('educational degree name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            'is_academic': forms.Select(
                choices=models.IS_ACADEMIC_CHOICES
            ),
            "description": get_textarea_field(
                placeholder=_("educational degree's description")
            ),
        }
