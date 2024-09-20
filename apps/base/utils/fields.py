from django.db import models
from django.shortcuts import get_object_or_404
from django import forms
from django.forms.widgets import Widget
from django.urls import reverse


def get_search_input(
    widget: Widget,
    form: forms.ModelForm,
    url_name: str,
    field_name: str,
    model: models.Model,
    value_attributes: list[str] = [],
    required: bool = False,
    multiple: bool = False,
):
    """
    use it inside ModelForm.__init__() method  
    widget: Widget like `CheckboxInput`  
    form: ModelForm like `self`  
    url_name: str like `departments:search`  
    field_name: str like `parent`  
    model: Model like `Department`  
    value: list[str] = [] like `f'{parent_obj.department_id} - {parent_obj.name}'`
    required: bool = False  
    multiple: bool = False  
    """
    hx_get_path = f'{reverse(url_name)}?name={field_name}'

    field = form.initial.get(field_name)
    field = form.data.get(field_name, field)

    if field and value_attributes:
        obj = get_object_or_404(model, id=field)
        values = [getattr(obj, attr) for attr in value_attributes]
        value = " - ".join(values)
    
    if field:
        hx_get_path += f'&id={field}&value={value}'
    
    if required: 
        hx_get_path += "&required=true"
        
    if multiple: 
        hx_get_path += "&multiple=true"
    
    return widget({
        "hx-get": hx_get_path ,
        "hx-trigger": "load",
        "hx-target": "this",
        "style": "display: none;",
    })