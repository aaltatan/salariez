from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

class JobSubtypeForm(forms.ModelForm):
    
    class Meta:
        model = models.JobSubtype
        fields = ['name', 'job_type', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('job subtype name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            'job_type': forms.Select({
                'data_add_new': '/job-types/create/?modal=true',
                'data_permission': 'job_types.add_jobtype',
                'data_hx_target': '#modal'
            }),
            "description": forms.Textarea(
                attrs={
                    "x-autosize": "",
                    "rows": "1",
                    "autocomplete": "on",
                    "placeholder": _("job subtype's description"),
                }
            ),
        }