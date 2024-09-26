from dataclasses import dataclass

from django.db import models
from django.shortcuts import get_object_or_404
from django import forms
from django.forms.widgets import Widget
from django.urls import reverse

from icecream import ic


@dataclass
class Object:
    model: models.Model
    url_name: str
    field_name: str
    value_attributes: list[str]
    required: bool = False
    multiple: bool = False
    is_modal: bool = False
    add_new_url: tuple[str, str] | None = None


def get_search_input(
    widget: Widget,
    form: forms.ModelForm,
    obj: Object,
) -> Widget:
    """
    use it inside ModelForm.__init__() method  
    widget: select what widget will present the field form `django.forms.widgets`  
    form: ModelForm like `self`  
    obj: Object  
    """
    hx_get_path = f'{reverse(obj.url_name)}?name={obj.field_name}'

    field = form.initial.get(obj.field_name)
    field = form.data.get(obj.field_name, field)

    if field and obj.value_attributes:
        instance = get_object_or_404(obj.model, id=field)
        values = [
            getattr(instance, attr) for attr in obj.value_attributes
        ]
        value = " - ".join(values)
    
    if field:
        hx_get_path += f'&id={field}&value={value}'
    
    if obj.required: 
        hx_get_path += "&required=true"
    
    if obj.multiple: 
        hx_get_path += "&multiple=true"
        
    attributes = {
        "hx-get": hx_get_path ,
        "hx-trigger": "load",
        "hx-target": "this",
        "style": "display: none;",
        "hx-replace-url": "false",
    }

    if obj.add_new_url is not None:
        
        url, permission = obj.add_new_url

        url = reverse(url)
        if obj.is_modal:
            url += '?modal=true'
            attributes['data_hx_target'] = '#modal'

        attributes['data_add_new'] = url
        attributes['data_permission'] = permission
    
    return widget(attributes)