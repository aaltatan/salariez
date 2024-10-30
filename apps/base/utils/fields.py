from dataclasses import dataclass

from django import forms
from django.db import models
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.forms.widgets import (
    DateInput, TextInput, Widget, Textarea, FileInput
)

from ..widgets import TextWithDataListInput


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


def get_search_field(
    widget: Widget,
    form: forms.ModelForm,
    obj: Object,
) -> Widget:
    """
    use it inside ModelForm.__init__() method  
    like self.form.fields['<field_name>'].widget = get_search_input(...)
    widget: select what widget will present the field form `django.forms.widgets`
    form: ModelForm like `self`
    obj: Object
    """
    hx_get_path = f"{reverse(obj.url_name)}?name={obj.field_name}"

    field = form.initial.get(obj.field_name)
    field = form.data.get(obj.field_name, field)

    if field and obj.value_attributes:
        instance = get_object_or_404(obj.model, id=field)
        values = [getattr(instance, attr) for attr in obj.value_attributes]
        value = " - ".join(values)

    if field:
        hx_get_path += f"&id={field}&value={value}"

    if obj.required:
        hx_get_path += "&required=true"

    if obj.multiple:
        hx_get_path += "&multiple=true"

    attributes = {
        "hx-get": hx_get_path,
        "hx-trigger": "load",
        "hx-target": "this",
        "style": "display: none;",
        "hx-replace-url": "false",
    }

    if obj.add_new_url is not None:
        url, permission = obj.add_new_url

        url = reverse(url)
        if obj.is_modal:
            url += "?modal=true"
            attributes["data_hx_target"] = "#modal"

        attributes["data_add_new"] = url
        attributes["data_permission"] = permission

    return widget(attributes)


def get_date_field(
    required: bool = True,
    fill_on_focus: bool = True,
    placeholder: str = 'YYYY-MM-DD',
    **kwargs: dict[str, str],
) -> DateInput:
    
    attrs: dict[str, str] = {
        "x-mask": "9999-99-99",
        "placeholder": placeholder,
        "minlength": "10",
        "@keydown.Alt.Down.prevent": 'handleDateInputAltKeyDown($el, "up")',
        "@keydown.Alt.Up.prevent": 'handleDateInputAltKeyDown($el, "down")',
        "@keydown.Down.prevent": 'handleDateInputKeyDown($el, "up")',
        "@keydown.Up.prevent": 'handleDateInputKeyDown($el, "down")',
        "@dblclick": 'handleDateInputDblClick',
        "title": _("use down/up arrows to increase/decrease days\nuse Alt key + down/up arrows to increase/decrease years\nclick double to insert date of today"),
        **kwargs
    }

    if fill_on_focus:
        attrs["@focus"] = 'handleDateInputFocus'

    if required:
        attrs['required'] = ''

    return DateInput(attrs, format="%Y-%m-%d")


def get_numeric_field(
    count: int, required: bool = True, **kwargs: dict[str, str]
) -> TextInput:

    if count < 1:
        count = 1
    
    attrs: dict[str, str] = {
        "x-mask": "9" * count,
        **kwargs
    }

    if required:
        attrs['required'] = ''

    return TextInput(attrs)


def get_textarea_field(rows: int = 1, **kwargs) -> Textarea:

    if rows < 1:
        rows = 1
    
    return forms.Textarea({
        "x-autosize": "",
        "rows": str(rows),
        "autocomplete": "on",
        **kwargs
    })


def get_money_field(
    required: bool = False, 
    decimal_places: int = 2, 
    **kwargs
) -> TextInput:

    attrs = {
        'type': 'text',
        'x-mask:dynamic': f'$money($input, ".", ",", {decimal_places})',
        **kwargs
    }

    if required:
        attrs['required'] = ''

    return TextInput(attrs)


def get_avatar_field(
    url: str, **kwargs: dict[str, str]
) -> FileInput:

    attrs = {
        'hx-get': reverse_lazy(url, kwargs=kwargs),
        'hx-trigger': 'load',
        'hx-target': 'this',
    }

    return FileInput(attrs)

def get_input_datalist(
    model: models.Model, field_name: str, attrs=None
) -> TextWithDataListInput:

    return TextWithDataListInput(
        attrs=attrs,
        datalist=list(set(
            model.objects.values_list(field_name, flat=True).order_by(field_name)
        ))
    )