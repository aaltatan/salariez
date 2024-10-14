from django import forms
from django.utils.translation import gettext as _

from .. import models

from apps.base.widgets import SearchWidget
from apps.base.utils.generic import parse_decimals
from apps.base.utils.fields import (
    get_date_field, 
    get_numeric_field, 
    get_textarea_field,
    get_avatar_field,
)


class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model = models.Employee
        fields = '__all__'
        widgets = {
            'address': forms.widgets.TextInput({
                'autocomplete': 'off'
            }),
            'notes': get_textarea_field(
                rows=2, placeholder=_("notes")
            ),
            'profile': get_avatar_field(
                'base:fields-avatar', id='id_profile', name='profile'
            ),
            'salary': forms.widgets.TextInput({
                'type': 'text',
                'x-mask:dynamic': '$money($input, ".", ",", 2)'
            }),
            # --- search fields ----
            'area': SearchWidget(),
            'department': SearchWidget(),
            'position': SearchWidget(),
            # --- date fields ----
            'birth_date': get_date_field(),
            'card_date': get_date_field(required=False),
            'hire_date': get_date_field(),
            # --- numeric fields ----
            'national_id': get_numeric_field(
                20, placeholder=_('national id').title()
            ),
            'card_id': get_numeric_field(
                20, placeholder=_('card id').title()
            ),
            'institution_id': get_numeric_field(
                count=20, 
                required=False, 
                placeholder=_('institution id').title()
            ),
            'registry_office_id': get_numeric_field(
                20, 
                required=False,
                placeholder=_('registry office id').title()
            ),
        }

    def __init__(self, data = None, *args, **kwargs) -> None:

        if data:
            data = data.copy()
            data['salary'] = parse_decimals(data['salary'])

        super().__init__(data, *args, **kwargs)
