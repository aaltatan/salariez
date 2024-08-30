from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from . import models, forms, mixins, resources

from apps.base.mixins import (
    CreateMixin,
    DeleteMixin,
    UpdateMixin,
    SearchMixin,
    ExportMixin,
)


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
    LoginRequiredMixin, PermissionRequiredMixin, View,
):
    
    permission_required = 'departments.view_department'
    model = models.Department
    
    def _get_app_label(self) -> str:
        
        return self.model._meta.app_label
    
    def _get_template_name(self) -> str:
        
        if getattr(self, 'template_name', None) is not None:
            return self.template_name
        
        app_label = self._get_app_label()
        return f'apps/{app_label}/index.html'
    
    def _get_body_template_name(self) -> str:
        
        if getattr(self, 'body_template_name', None) is not None:
            return self.body_template_name
        
        app_label = self._get_app_label()
        return f'apps/{app_label}/partials/body.html'
    
    def get(self, request, *args, **kwargs):
        
        qs = self.model.objects.all()
        context = {'qs': qs}
        
        template_name = self._get_body_template_name()
        
        if not request.htmx or request.htmx.boosted:
            template_name = self._get_template_name()
        
        return render(request, template_name, context)


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
