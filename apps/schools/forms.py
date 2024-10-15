from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import get_textarea_field
from apps.base.widgets import SearchWidget


class SchoolForm(forms.ModelForm):
    
    class Meta:
        model = models.School
        fields = ['name', 'nationality', 'school_type', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('school name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            "nationality": SearchWidget(),
            "school_type": SearchWidget(),
            "description": get_textarea_field(
                placeholder=_("school's description")
            ),
        }
