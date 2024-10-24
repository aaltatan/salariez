from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from braces.views import MultiplePermissionsRequiredMixin

from .. import forms
from ..models import Employee

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
            'employees.change_mobile',
            'employees.delete_mobile',
        ),
    }
    parent_model = Employee
    form_class = forms.MobileForm

    def post_save(self, instance):
        return

class EmailFormSetView(
    LoginRequiredMixin, 
    MultiplePermissionsRequiredMixin, 
    FormSetMixin, 
    View,
):
    permissions = {
        'all': (
            'employees.change_employee', 
            'employees.change_email',
            'employees.delete_email',
        ),
    }
    parent_model = Employee
    form_class = forms.EmailForm

    def post_save(self, instance):
        return

class PhoneFormSetView(
    LoginRequiredMixin, 
    MultiplePermissionsRequiredMixin, 
    FormSetMixin, 
    View,
):
    permissions = {
        'all': (
            'employees.change_employee', 
            'employees.change_phone',
            'employees.delete_phone',
        ),
    }
    parent_model = Employee
    form_class = forms.PhoneForm

    def post_save(self, instance):
        return

class EducationalTransactionFormSetView(
    LoginRequiredMixin, 
    MultiplePermissionsRequiredMixin, 
    FormSetMixin, 
    View,
):
    permissions = {
        'all': (
            'employees.change_employee', 
            'employees.change_educationtransaction',
            'employees.delete_educationtransaction',
        ),
    }
    parent_model = Employee
    form_class = forms.EducationTransactionForm
    
    def post_save(self, instance):

        Klass = self.get_model_class()

        not_current_count = \
              Klass.objects.filter(employee=instance, is_current=False).count()
        all_count = Klass.objects.filter(employee=instance).count()
        
        if all_count and all_count == not_current_count:
            obj = Klass.objects.filter(employee=instance).order_by('order').last()
            obj.is_current = True
            obj.save()

class ContractFormSetView(
    LoginRequiredMixin, 
    MultiplePermissionsRequiredMixin, 
    FormSetMixin, 
    View,
):
    permissions = {
        'all': (
            'employees.change_employee', 
            'employees.change_contract',
            'employees.delete_contract',
        ),
    }
    parent_model = Employee
    form_class = forms.ContractForm
    
    def post_save(self, instance):
        pass