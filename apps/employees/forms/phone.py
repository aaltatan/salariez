from django import forms

from ..models import Phone

from apps.base.utils.fields import get_textarea_field


class PhoneForm(forms.ModelForm):

    class Meta:
        model = Phone
        fields = ['phone', 'notes']
        widgets = {
            'notes': get_textarea_field()
        }