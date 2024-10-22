from django import forms
from django.utils.translation import gettext as _

from ..models import Employee

from apps.base.widgets import SearchWidget
from apps.base.utils.fields import (
    get_date_field, 
    get_numeric_field, 
    get_textarea_field,
    get_avatar_field,
)


class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'address': forms.widgets.TextInput({
                'autocomplete': 'off'
            }),
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

