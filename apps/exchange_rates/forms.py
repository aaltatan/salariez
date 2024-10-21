from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import get_textarea_field


class ExchangeRateForm(forms.ModelForm):
    
    class Meta:
        model = models.ExchangeRate
        fields = ['name', 'notes']
        widgets = {
            "notes": get_textarea_field(
                placeholder=_("notes")
            ),
        }
