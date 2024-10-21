from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import (
    get_textarea_field, get_date_field
)


class ExchangeRateForm(forms.ModelForm):

    currency = forms.ModelChoiceField(
        models.Currency.objects.filter(is_local__exact=False)
    )
    
    class Meta:
        model = models.ExchangeRate
        fields = [
            'currency', 
            'input_rate',
            'is_inverse',
            'date',
            'bulletin_number',
            'notes',
        ]
        widgets = {
            "date": get_date_field(),
            "notes": get_textarea_field(
                placeholder=_("notes")
            ),
        }
