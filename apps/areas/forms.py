from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from . import models

from apps.base.utils.fields import (
    Object, 
    get_search_field, 
    get_textarea_field,
)



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
            is_modal=True,
            add_new_url=('cities:create', 'cities.add_city')
        )

        self.fields['city'].widget = get_search_field(
            widget=widgets.TextInput,
            form=self, 
            obj=city,
        )