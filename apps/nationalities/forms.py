from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class NationalityForm(forms.ModelForm):
    
    class Meta:
        model = models.Nationality
        fields = ['name', 'is_local', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('nationality name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            'is_local': forms.Select(choices=models.IS_LOCAL_CHOICES),
            "description": forms.Textarea({
                "x-autosize": "",
                "rows": "1",
                "autocomplete": "on",
                "placeholder": _("nationality's description"),
            }),
        }