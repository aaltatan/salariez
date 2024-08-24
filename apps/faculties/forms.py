from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

class FacultyForm(forms.ModelForm):
    
    class Meta:
        model = models.Faculty
        fields = ['name']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('faculty name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            })
        }
