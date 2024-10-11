from django.views.generic import ListView, View, RedirectView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from braces.views import SuperuserRequiredMixin

from . import models, forms, filters, mixins, resources, utils

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


class SearchView(LoginRequiredMixin, SearchMixin, View):
    
    model = models.Status
    input_placeholder = _('search status')


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'statuses.view_status'
    
    filter_class = filters.StatusFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('statuses:index'),
        'hx-target': '#statuses-table',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'statuses.can_export'
    resource_class = resources.StatusRecourse
    filter_class = filters.StatusFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'statuses:bulk-delete',
        'bulk_reslugify': 'statuses:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'statuses:delete_status'
    model = models.Status


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.Status
    bulk_path = 'statuses:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'statuses.add_status'
    form_class = forms.StatusForm


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View
):
    
    permission_required = 'statuses.change_status'
    form_class = forms.StatusForm
    deleter = utils.Deleter


class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'statuses.delete_status'
    model = models.Status
    deleter = utils.Deleter