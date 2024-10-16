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

from .. import (
    models, forms, filters, mixins, resources, utils
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
    'position',
    'status',
    'job_subtype',
    'job_subtype__job_type',
    'department',
    'department__cost_center',
]
prefetch_related: list[str] = [
    'mobiles', 'phones', 'emails', 'education_transactions'
]


class EmployeeDetailView(DetailView):

    model = models.Employee
    template_name = 'apps/employees/details.html'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(*select_related)
            .prefetch_related(*prefetch_related)
        )


class SearchView(LoginRequiredMixin, SearchMixin, View):
    
    model = models.Employee
    input_placeholder = _('search employee')


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'employees.view_employee'

    sortable_by = OrderList([
        OrderItem(_('has salary'), '-status__has_salary', checked=True),
        OrderItem(_('department id'), 'department__department_id', checked=True),
        OrderItem(_('job type'), 'job_subtype__job_type', checked=True),
        OrderItem(_('job subtype'), 'job_subtype', checked=True),
        OrderItem(_('firstname'), 'firstname', checked=True),
        OrderItem(_('gender'), 'gender'),
        OrderItem(_('department name'), 'department'),
        OrderItem(_('position'), 'position'),
        OrderItem(_('status'), 'status'),
        OrderItem(_('hire date'), 'hire_date'),
        OrderItem(_('birth date'), 'birth_date'),
        OrderItem(_('salary'), 'salary'),
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
    form_template_name = 'apps/employees/partials/forms/create.html'
    

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
    model = models.Employee
    deleter = utils.Deleter