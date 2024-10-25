from django import forms
from django.utils.translation import gettext as _

from ..models import Employee

from apps.base.widgets import (
    SearchWidget, MultipleSelectWidget
)
from apps.base.utils.fields import (
    get_date_field, 
    get_numeric_field, 
    get_textarea_field,
    get_avatar_field,
    get_input_datalist,
)


class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'firstname': get_input_datalist(Employee, 'firstname'),
            'lastname': get_input_datalist(Employee, 'lastname'),
            'father_name': get_input_datalist(Employee, 'father_name'),
            'mother_name': get_input_datalist(Employee, 'mother_name'),
            'birth_place': get_input_datalist(Employee, 'birth_place'),
            'civil_registry_office': get_input_datalist(
                Employee, 'civil_registry_office'
            ),
            'registry_office_name': get_input_datalist(
                Employee, 'registry_office_name'
            ),
            'face_color': get_input_datalist(Employee, 'face_color'),
            'eyes_color': get_input_datalist(Employee, 'eyes_color'),
            'address': get_input_datalist(
                Employee, 'address', {'autocomplete': 'off'}
            ),
            'special_signs': get_input_datalist(
                Employee, 'special_signs'
            ),
            'groups': MultipleSelectWidget(),
            'notes': get_textarea_field(
                rows=1, placeholder=_("notes")
            ),
            'profile': get_avatar_field(
                'base:fields-avatar', id='id_profile', name='profile'
            ),
            # --- search fields ----
            'area': SearchWidget(),
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

