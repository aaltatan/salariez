from django import forms
from django.db.models import TextChoices


class PaginatedByForm(forms.Form):
    
    class PaginationChoices(TextChoices):
        TEN = '10', '10'
        TWENTY_FIVE = '25', '25'
        FIFTY = '50', '50'
        ALL = 'all', 'All'
    
    per_page = forms.ChoiceField(
        choices=PaginationChoices.choices,
        required=False,
        initial=PaginationChoices.TEN,
        label=''
    )
    
    def __init__(self, attrs: dict, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
            
        self.fields['per_page'].widget.attrs['class'] = (
            'py-2 pl-2 pr-8 rounded-lg bg-gray-50 dark:bg-gray-900 outline-none focus:ring-1 focus:ring-blue-500 border-none duration-150'
        )
        self.fields['per_page'].widget.attrs['hx-include'] = '[data-include]'
        self.fields['per_page'].widget.attrs['data-include']= ''
        
        for k, v in attrs.items():
            self.fields['per_page'].widget.attrs[k] = v