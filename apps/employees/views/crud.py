from django.views.generic import ListView, View, RedirectView, DetailView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from braces.views import (
    SuperuserRequiredMixin,
)

from ..models import Employee
from .. import (
    forms, filters, mixins, resources, utils
)

from apps.base.utils.generic import OrderList, OrderItem
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


select_related: list[str] = [
    'area',
]
prefetch_related: list[str] = [
    'mobiles', 'phones', 'emails', 'education_transactions'
]


class EmployeeDetailView(DetailView):

    model = Employee
    template_name = 'apps/employees/details.html'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(*select_related)
            .prefetch_related(*prefetch_related)
        )


class SearchView(LoginRequiredMixin, SearchMixin, View):
    
    model = Employee
    input_placeholder = _('search employee')


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'employees.view_employee'

    sortable_by = OrderList([
        OrderItem(_('firstname'), 'firstname', checked=True),
        OrderItem(_('gender'), 'gender'),
        OrderItem(_('hire date'), 'hire_date'),
        OrderItem(_('birth date'), 'birth_date'),
        OrderItem(_('education degree'), 'education_order'),
    ])
    filter_class = filters.EmployeeFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('employees:index'),
        'hx-target': '#employees-table #container > div',
    }

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(*select_related)
            .prefetch_related(*prefetch_related)
        )


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
    model = Employee


class BulkReslugifyView(
    LoginRequiredMixin, 
    SuperuserRequiredMixin, 
    BulkModalMixin,
    ReslugifyModalMixin,
    View
):
    model = Employee
    bulk_path = 'employees:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'employees.add_employee'
    form_class = forms.EmployeeForm
    form_template_name = 'apps/employees/partials/forms/create.html'
    continue_updating = True
    

class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View
):
    
    permission_required = 'employees.change_employee'
    form_class = forms.EmployeeForm
    deleter = utils.Deleter
    form_template_name = 'apps/employees/partials/forms/update.html'


class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'employees.delete_employee'
    model = Employee
    deleter = utils.Deleter