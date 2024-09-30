from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import get_textarea_field


class CostCenterForm(forms.ModelForm):
    
    class Meta:
        model = models.CostCenter
        fields = ['name', 'cost_center_accounting_id', 'description']
        widgets = {
            'name': forms.TextInput({
                'placeholder': _('cost center name'),
                'autofocus': 'true',
                'autocomplete': 'off',
            }),
            'cost_center_accounting_id': forms.TextInput({
                'placeholder': _('cost center description'),
                'x-mask': '9999999999',
                'autocomplete': 'off',
            }),
            "description": get_textarea_field(
                placeholder=_("cost center's description")
            ),
        }
