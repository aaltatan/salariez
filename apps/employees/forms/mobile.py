from django import forms
from django.utils.translation import gettext as _

from ..models import Mobile

from apps.base.utils.fields import get_textarea_field


HAS_WHATSAPP_CHOICES = (
    (True, _('yes').title()),
    (False, _('no').title()),
)

class MobileForm(forms.ModelForm):

    class Meta:
        model = Mobile
        fields = ['mobile', 'has_whatsapp', 'notes']
        widgets = {
            'mobile': forms.widgets.TextInput({
                'x-mask': '9999999999'
            }),
            'has_whatsapp': forms.widgets.Select(
                choices=HAS_WHATSAPP_CHOICES
            ),
            'notes': get_textarea_field()
        }