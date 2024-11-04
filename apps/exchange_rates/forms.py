from django import forms
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.widgets import DynamicDateInputWidget
from apps.base.utils.fields import get_textarea_field


IS_INVERSE_CHOICES = (
    (False, _('regular').title()),
    (True, _('inverse').title()),
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
            "is_inverse": forms.widgets.Select(choices=IS_INVERSE_CHOICES),
            "date": DynamicDateInputWidget(),
            "notes": get_textarea_field(
                placeholder=_("notes")
            ),
        }
