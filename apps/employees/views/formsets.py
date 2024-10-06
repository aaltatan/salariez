from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from braces.views import MultiplePermissionsRequiredMixin

from .. import models, forms

from apps.base.mixins import FormSetMixin


class MobileFormSetView(
    LoginRequiredMixin, 
    MultiplePermissionsRequiredMixin, 
    FormSetMixin, 
    View,
):
    permissions = {
        'all': (
            'employees.change_employee', 
            'mobiles.change_mobile',
            'mobiles.delete_mobile',
        ),
    }
    parent_model = models.Employee
    form_class = forms.MobileForm


class EmailFormSetView(
    LoginRequiredMixin, 
    MultiplePermissionsRequiredMixin, 
    FormSetMixin, 
    View,
):
    permissions = {
        'all': (
            'employees.change_employee', 
            'emails.change_email',
            'emails.delete_email',
        ),
    }
    parent_model = models.Employee
    form_class = forms.EmailForm


class PhoneFormSetView(
    LoginRequiredMixin, 
    MultiplePermissionsRequiredMixin, 
    FormSetMixin, 
    View,
):
    permissions = {
        'all': (
            'employees.change_employee', 
            'phones.change_phone',
            'phones.delete_phone',
        ),
    }
    parent_model = models.Employee
    form_class = forms.PhoneForm