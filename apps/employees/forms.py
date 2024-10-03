from django import forms
from django.utils.translation import gettext as _

from . import models
from apps.base.utils.generic import parse_decimals
from apps.base.utils.fields import (
    Object,
    get_date_field, 
    get_numeric_field, 
    get_textarea_field,
    get_avatar_field,
    get_search_field,
)


class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model = models.Employee
        fields = '__all__'
        widgets = {
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

        area = Object(
            model=models.employee.Area,
            url_name='areas:search',
            field_name='area',
            add_new_url=('areas:create', 'areas.add_area'),
            required=True,
            value_attributes=['name'],
        )
        self.fields['area'].widget = get_search_field(
            widget=forms.widgets.TextInput,
            form=self,
            obj=area
        )

        department = Object(
            model=models.employee.Department,
            url_name='departments:search',
            field_name='department',
            add_new_url=('departments:create', 'departments.add_department'),
            required=True,
            value_attributes=['name'],
        )
        self.fields['department'].widget = get_search_field(
            widget=forms.widgets.TextInput,
            form=self,
            obj=department
        )

        position = Object(
            model=models.employee.Position,
            url_name='positions:search',
            field_name='position',
            is_modal=True,
            add_new_url=('positions:create', 'positions.add_position'),
            required=True,
            value_attributes=['name'],
        )
        self.fields['position'].widget = get_search_field(
            widget=forms.widgets.TextInput,
            form=self,
            obj=position
        )
