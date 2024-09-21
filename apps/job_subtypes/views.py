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
)


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'job_subtypes.view_jobsubtype'
    
    model = models.JobSubtype
    filter_class = filters.JobSubtypeFilterSet
    
    template_name = 'apps/job_subtypes/partials/table.html'
    index_template_name = 'apps/job_subtypes/index.html'
    
    paginate_by_form = base_forms.PaginatedByForm
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('job_subtypes:index'),
        'hx-target': '#job-subtypes-table',
    }
    
    def get_queryset(self):
        return super().get_queryset().select_related('job_type')


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'job_subtypes.can_export'
    resource_class = resources.JobSubtypeRecourse
    filter_class = filters.JobSubtypeFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'job_subtypes:bulk-delete',
        'bulk_reslugify': 'job_subtypes:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'job_subtypes:delete_jobsubtype'
    model = models.JobSubtype


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.JobSubtype
    bulk_path = 'job_subtypes:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'job_subtypes.add_jobsubtype'
    form_class = forms.JobSubtypeForm
    

class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View
):
    
    permission_required = 'job_subtypes.change_jobsubtype'
    form_class = forms.JobSubtypeForm
    deleter = utils.Deleter

class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'job_subtypes.delete_jobsubtype'
    model = models.JobSubtype
    deleter = utils.Deleter