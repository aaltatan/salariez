from django import forms

from ..models import Contract

from apps.base.widgets import SearchWidget
from apps.base.utils.generic import parse_decimals
from apps.base.utils.fields import get_date_field, get_money_field


class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = [
          'department', 
          'job_subtype', 
          'status', 
          'position', 
          'contract_type', 
          'ownership', 
          'salary', 
          'start_date', 
          'end_date', 
          'institution_id', 
        ]
        widgets = {
            'department': SearchWidget(),
            'job_subtype': SearchWidget(),
            'status': SearchWidget(),
            'position': SearchWidget(),
            'salary': get_money_field(required=True),
            'start_date': get_date_field(required=False),
            'end_date': get_date_field(
                required=False, fill_on_focus=False
            ),
        }
        
    def __init__(self, data = None, *args, **kwargs) -> None:

        if data:
            data: dict = data.copy()
            data = {
                k: parse_decimals(v) if k.endswith('salary') else v
                for k,v in data.items()
            }

        super().__init__(data, *args, **kwargs)