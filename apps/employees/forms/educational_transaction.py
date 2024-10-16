from django import forms

from ..models import EducationTransaction

from apps.base.widgets import SearchWidget
from apps.base.utils.fields import get_date_field


class EducationTransactionForm(forms.ModelForm):

    class Meta:
        model = EducationTransaction
        fields = [
            'employee', 
            'degree', 
            'specialization',
            'school',
            'order',
            'graduation_date',
            'is_current',
        ]
        widgets = {
            'employee': SearchWidget(),
            'degree': SearchWidget({'autofocus': 'on'}),
            'specialization': SearchWidget(),
            'school': SearchWidget(),
            'graduation_date': get_date_field(
                required=False, fill_on_focus=False
            ),
        }