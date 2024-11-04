from django import forms

from ..models import EducationTransaction

from apps.base.widgets import SearchWidget, DynamicDateInputWidget


class EducationTransactionForm(forms.ModelForm):

    class Meta:
        model = EducationTransaction
        fields = [
            'degree', 
            'specialization',
            'school',
            'order',
            'graduation_date',
            'is_current',
        ]
        widgets = {
            'degree': SearchWidget(),
            'specialization': SearchWidget(),
            'school': SearchWidget(),
            'graduation_date': DynamicDateInputWidget(
                {'required': False}, fill_on_focus=False
            ),
        }