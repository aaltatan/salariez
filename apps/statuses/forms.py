from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class StatusForm(forms.ModelForm):
    
    class Meta:
        model = models.Status
        fields = ['name', 'has_salary', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('status name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            'has_salary': forms.Select(choices=models.HAS_SALARY_CHOICES),
            "description": forms.Textarea({
                "x-autosize": "",
                "rows": "1",
                "autocomplete": "on",
                "placeholder": _("status's description"),
            }),
        }