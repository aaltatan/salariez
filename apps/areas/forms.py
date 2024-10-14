from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.widgets import SearchWidget
from apps.base.utils.fields import get_textarea_field


class AreaForm(forms.ModelForm):
    
    class Meta:
        model = models.Area
        fields = ['name', 'city', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('area name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            "description": get_textarea_field(
                placeholder=_("area's description")
            ),
            "city": SearchWidget(),
        }