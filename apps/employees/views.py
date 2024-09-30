from django.views.generic import ListView, View, RedirectView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from braces.views import SuperuserRequiredMixin

from . import models, forms, filters, mixins, resources, utils

from apps.base import forms as base_forms
from apps.base.mixins import (
    ListMixin,
    CreateMixin,
    UpdateMixin,
    DeleteMixin,
    BulkModalMixin,
    BulkMapperMixin,
    ReslugifyModalMixin,
    SearchMixin,
    ExportMixin,
)


class SearchView(LoginRequiredMixin, SearchMixin, View):
    
    model = models.Employee
    input_placeholder = _('search employee')


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'employees.view_employee'
    
    model = models.Employee
    filter_class = filters.EmployeeFilterSet
    
    template_name = 'apps/employees/index.html'
    
    paginate_by_form = base_forms.PaginatedByForm
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('employees:index'),
        'hx-target': '#employees-table',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'employees.can_export'
    resource_class = resources.EmployeeRecourse
    filter_class = filters.EmployeeFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'employees:bulk-delete',
        'bulk_reslugify': 'employees:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'employees:delete_employee'
    model = models.Employee


class BulkReslugifyView(
    LoginRequiredMixin, 
    SuperuserRequiredMixin, 
    BulkModalMixin,
    ReslugifyModalMixin,
    View
):
    model = models.Employee
    bulk_path = 'employees:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'employees.add_employee'
    form_class = forms.EmployeeForm
    form_template_name = 'apps/employees/partials/create-form.html'
    

class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View
):
    
    permission_required = 'employees.change_employee'
    form_class = forms.EmployeeForm
    deleter = utils.Deleter


class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'employees.delete_employee'
    model = models.Employee
    deleter = utils.Deleter