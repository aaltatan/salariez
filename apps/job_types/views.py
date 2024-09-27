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
    ExportMixin,
    SearchMixin,
)


class SearchView(LoginRequiredMixin, SearchMixin, View):
    
    model = models.JobType
    input_placeholder = _('search job type')


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'job_types.view_jobtype'
    
    model = models.JobType
    filter_class = filters.JobTypeFilterSet
    
    template_name = 'apps/job_types/index.html'
    
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
        'bulk_delete': 'job_types:bulk-delete',
        'bulk_reslugify': 'job_types:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'job_types:delete_jobtype'
    model = models.JobType


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.JobType
    bulk_path = 'job_types:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'job_types.add_jobtype'
    form_class = forms.JobTypeForm


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View
):
    
    permission_required = 'job_types.change_jobtype'
    form_class = forms.JobTypeForm
    deleter = utils.Deleter


class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'job_types.delete_jobtype'
    model = models.JobType
    deleter = utils.Deleter