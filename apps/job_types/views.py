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
    
    permission_required = 'job_types.view_job_type'
    
    model = models.JobType
    filter_class = filters.JobTypeFilterSet
    
    template_name = 'apps/job_types/partials/table.html'
    index_template_name = 'apps/job_types/index.html'
    
    paginate_by_form = base_forms.PaginatedByForm
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('job_types:index'),
        'hx-target': '#job-types-table',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'job_types.can_export'
    resource_class = resources.JobTypeRecourse
    filter_class = filters.JobTypeFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'job_types:bulk-delete'
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'job_types:delete_job_type'
    model = models.JobType
    hx_location_target = '#job-types-table'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'job_types.add_job_type'
    form_class = forms.JobTypeForm
    template_name = 'apps/job_types/create.html'
    

class UpdateView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    UpdateMixin, 
    mixins.CannotDeleteMixin, 
    View
):
    
    permission_required = 'job_types.change_job_type'
    form_class = forms.JobTypeForm
    template_name = 'apps/job_types/update.html'


class DeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    DeleteMixin, 
    mixins.CannotDeleteMixin, 
    View
):

    permission_required = 'job_types.delete_job_type'
    model = models.JobType
    hx_location_target = '#job-types-table'