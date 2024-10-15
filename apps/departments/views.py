from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, RedirectView
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from braces.views import SuperuserRequiredMixin

from . import models, forms, resources, utils, filters

from apps.base.utils.generic import OrderItem, OrderList
from apps.base.mixins import (
    BulkModalMixin,
    ReslugifyModalMixin,
    BulkMapperMixin,
    CreateMixin,
    DeleteMixin,
    UpdateMixin,
    ExportMixin,
    ListMixin,
)


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_reslugify': 'departments:bulk-reslugify',
    }


class BulkReslugifyView(
    LoginRequiredMixin, 
    SuperuserRequiredMixin, 
    BulkModalMixin,
    ReslugifyModalMixin,
    View
):
    model = models.Department
    bulk_path = 'departments:bulk-reslugify'


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View,
):
    
    permission_required = 'departments.can_export'
    resource_class = resources.DepartmentResource


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'departments.view_department'
    sortable_by = OrderList([
        OrderItem(_('code'), 'department_id', checked=True),
        OrderItem(_('parent'), 'parent'),
        OrderItem(_('level'), 'level'),
        OrderItem(_('cost center'), 'cost_center__cost_center_accounting_id'),
    ])
    filter_class = filters.DepartmentFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('departments:index'),
        'hx-target': '#departments-table #container > div',
    }
    
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('cost_center', 'parent')
        )


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'departments.add_department'
    form_class = forms.DepartmentCreateForm


class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View,
):
    
    permission_required = 'departments.delete_department'
    model = models.Department
    deleter = utils.Deleter


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View,
):
    
    permission_required = 'departments.update_department'
    form_class = forms.DepartmentUpdateForm
    deleter = utils.Deleter