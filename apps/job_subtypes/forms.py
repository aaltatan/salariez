from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.widgets import SearchWidget
from apps.base.utils.fields import get_textarea_field


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
            'job_type': SearchWidget({
                'data_add_new': '/job-types/create/?modal=true',
                'data_permission': 'job_types.add_jobtype',
                'data_hx_target': '#modal'
            }),
            "description": get_textarea_field(
                placeholder=_("job subtype's description")
            ),
        }