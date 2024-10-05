from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, RedirectView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from braces.views import SuperuserRequiredMixin

from . import models, forms, resources, utils, filters
from apps.base import forms as base_forms

from apps.base.mixins import (
    BulkModalMixin,
    ReslugifyModalMixin,
    BulkMapperMixin,
    CreateMixin,
    DeleteMixin,
    UpdateMixin,
    SearchMixin,
    ExportMixin,
    ListMixin,
)


class SearchView(
    LoginRequiredMixin, SearchMixin, View,
):
    
    model = models.Department
    input_placeholder = _('search department')

    def get_queryset(self):
        return super().get_queryset().order_by('department_id')


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
    
    model = models.Department
    filter_class = filters.DepartmentFilterSet
    
    template_name = 'apps/departments/index.html'
    
    paginate_by_form = base_forms.PaginatedByForm
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('departments:index'),
        'hx-target': '#departments-table',
    }
    
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('cost_center', 'parent')
            .order_by('department_id')
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
    hx_location_target = '#departments-body'
    deleter = utils.Deleter


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View,
):
    
    permission_required = 'departments.update_department'
    form_class = forms.DepartmentUpdateForm
    deleter = utils.Deleter