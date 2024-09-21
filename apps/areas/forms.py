from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils import get_search_input, Object



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
            "description": forms.Textarea({
                "x-autosize": "",
                "rows": "1",
                "autocomplete": "on",
                "placeholder": _("area's description"),
            }),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # cities search field
        city = Object(
            url_name='cities:search', 
            field_name='city', 
            model=models.City,
            value_attributes=['name'],
            required=True,
            add_new_url=('cities:create', 'cities.add_city')
        )

        self.fields['city'].widget = get_search_input(
            widget=widgets.TextInput,
            form=self, 
            obj=city,
        )