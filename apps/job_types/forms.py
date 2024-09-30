from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import get_textarea_field


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
            "description": get_textarea_field(
                placeholder=_("job type's description")
            ),
        }
