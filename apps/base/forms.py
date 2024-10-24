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
            'py-1 pr-8 pl-2 rounded-md bg-neutral-50 dark:bg-neutral-900 outline-none focus:ring-1 focus:ring-blue-500 border-none duration-150 text-lg'
        )
        self.fields['per_page'].widget.attrs['hx-include'] = '[data-include]'
        self.fields['per_page'].widget.attrs['hx-replace-url'] = 'true'
        self.fields['per_page'].widget.attrs['hx-headers'] = '{"partial": true}'
        self.fields['per_page'].widget.attrs['data-include']= ''
        
        for k, v in attrs.items():
            self.fields['per_page'].widget.attrs[k] = v