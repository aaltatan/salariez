from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from braces.views import SuperuserRequiredMixin

from . import models, forms, resources, mixins, utils

from apps.base.mixins import (
    CreateMixin,
    DeleteMixin,
    UpdateMixin,
    SearchMixin,
    ExportMixin,
    TreeMixin,
    DebugRequiredMixin,
)


class EmptyView(
    SuperuserRequiredMixin, 
    DebugRequiredMixin,
    mixins.EmptyMixin, 
    View
):
    
    model = models.Department


class BulkCreateView(
    SuperuserRequiredMixin, mixins.BulkCreateMixin, View
):
    
    model = models.Department


class SearchView(
    LoginRequiredMixin, SearchMixin, View,
):
    
    model = models.Department
    input_placeholder = _('search department')


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View,
):
    
    permission_required = 'departments.can_export'
    resource_class = resources.DepartmentResource


class TreeView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    TreeMixin,
    View,
):
    
    permission_required = 'departments.view_department'
    model = models.Department
    
    def get_queryset(self):
        return super().get_queryset().select_related('cost_center')


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'departments.add_department'
    form_class = forms.DepartmentForm


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
    form_class = forms.DepartmentForm
    deleter = utils.Deleter