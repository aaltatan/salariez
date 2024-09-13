from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

class JobTypeForm(forms.ModelForm):
    
    class Meta:
        model = models.JobType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('job type name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            "description": forms.Textarea(
                attrs={
                    "x-autosize": "",
                    "rows": "1",
                    "autocomplete": "on",
                    "placeholder": _("job type's description"),
                }
            ),
        }
