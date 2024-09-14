from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from braces.views import SuperuserRequiredMixin

from . import models, forms, resources, mixins

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
    search_container_id = 'parent-departments-container'


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


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'departments.add_department'
    form_class = forms.DepartmentForm
    template_name = 'apps/departments/create.html'


class DeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    DeleteMixin, 
    mixins.CannotDeleteFacultyMixin, # locale mixin
    View,
):
    
    permission_required = 'departments.delete_department'
    model = models.Department
    hx_location_target = '#departments-body'


class UpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateMixin,
    View,
):
    
    permission_required = 'departments.update_department'
    form_class = forms.DepartmentForm
    template_name = 'apps/departments/update.html'