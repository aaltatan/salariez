from django import forms

from ..models import Email

from apps.base.utils.fields import get_textarea_field


class EmailForm(forms.ModelForm):

    class Meta:
        model = Email
        fields = ['email', 'notes']
        widgets = {
            'notes': get_textarea_field()
        }