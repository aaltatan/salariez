from typing import Iterable

from django.forms.widgets import (
    ChoiceWidget, SelectMultiple, Input, DateInput
)


class DynamicDateInputWidget(DateInput):
    template_name = 'widgets/date.html'

    def __init__(self, attrs = None, format = None, fill_on_focus: bool = True):
        self.fill_on_focus = fill_on_focus
        super().__init__(attrs, format)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['fill_on_focus'] = self.fill_on_focus
        return context


class TextWithDataListInputWidget(Input):
    input_type = "text"
    template_name = "widgets/text_datalist.html"

    def __init__(
        self, attrs=None, datalist: Iterable | None = None
    ) -> None:
        self.datalist = datalist
        super().__init__(attrs)
    
    def get_context(self, *args, **kwargs) -> dict:
        context = super().get_context(*args, **kwargs)
        context['datalist'] = self.datalist
        return context


class MultipleSelectWidget(SelectMultiple):
    template_name = "widgets/multiple.html"
    checked_attribute = {"checked": True}


class ComboboxWidget(SelectMultiple):
    template_name = "widgets/combobox.html"


class SearchWidget(ChoiceWidget):
    input_type = "select"
    template_name = "widgets/search.html"
    option_template_name = "widgets/search_item.html"
    add_id_index = False
    checked_attribute = {"checked": True}
    option_inherits_attrs = False

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if self.allow_multiple_selected:
            context["widget"]["attrs"]["multiple"] = True
        return context

    @staticmethod
    def _choice_has_empty_value(choice):
        """Return True if the choice's value is empty string or None."""
        value, _ = choice
        return value is None or value == ""

    def use_required_attribute(self, initial):
        """
        Don't render 'required' if the first <option> has a value, as that's
        invalid HTML.
        """
        use_required_attribute = super().use_required_attribute(initial)
        # 'required' is always okay for <select multiple>.
        if self.allow_multiple_selected:
            return use_required_attribute

        first_choice = next(iter(self.choices), None)
        return (
            use_required_attribute
            and first_choice is not None
            and self._choice_has_empty_value(first_choice)
        )