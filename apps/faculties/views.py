from django.views.generic import ListView, View, RedirectView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from . import models, forms, filters, mixins, resources

from apps.base import forms as base_forms
from apps.base.mixins import (
    ListMixin,
    CreateMixin,
    UpdateMixin,
    DeleteMixin,
    BulkModalMixin,
    BulkMapperMixin,
    ExportMixin,
)


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'faculties.view_faculty'
    
    model = models.Faculty
    filter_class = filters.FacultyFilterSet
    
    template_name = 'apps/faculties/partials/table.html'
    index_template_name = 'apps/faculties/index.html'
    
    paginate_by_form = base_forms.PaginatedByForm
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('faculties:index'),
        'hx-target': '#faculties-table',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'faculties.can_export'
    resource_class = resources.FacultyRecourse
    filter_class = filters.FacultyFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'faculties:bulk-delete'
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'faculties:delete_faculty'
    model = models.Faculty


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'faculties.add_faculty'
    form_class = forms.FacultyForm
    template_name = 'apps/faculties/create.html'
    

class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View
):
    
    permission_required = 'faculties.change_faculty'
    form_class = forms.FacultyForm
    template_name = 'apps/faculties/update.html'


class DeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    DeleteMixin, 
    mixins.CannotDeleteFacultyMixin, 
    View
):

    permission_required = 'faculties.delete_faculty'
    model = models.Faculty
