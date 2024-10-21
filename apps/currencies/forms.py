from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import get_textarea_field


class CurrencyForm(forms.ModelForm):
    
    class Meta:
        model = models.Currency
        fields = [
            'name', 
            'short_name', 
            'fraction_name', 
            'is_local', 
            'description',
        ]
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('currency name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            'short_name': forms.TextInput({
                'autocomplete': 'off',
                'placeholder': _('short name'),
            }),
            'fraction_name': forms.TextInput({
                'autocomplete': 'off',
                'placeholder': _('fraction name'),
            }),
            'is_local': forms.Select(choices=models.IS_LOCAL_CHOICES),
            "description": get_textarea_field(
                placeholder=_("currency's description")
            ),
        }