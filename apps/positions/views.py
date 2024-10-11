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
    
    model = models.Position
    input_placeholder = _('search position')


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'positions.view_position'
    
    filter_class = filters.PositionFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('positions:index'),
        'hx-target': '#positions-table',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'positions.can_export'
    resource_class = resources.PositionRecourse
    filter_class = filters.PositionFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'positions:bulk-delete',
        'bulk_reslugify': 'positions:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'positions:delete_position'
    model = models.Position


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.Position
    bulk_path = 'positions:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'positions.add_position'
    form_class = forms.PositionForm


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin,View
):
    
    permission_required = 'positions.change_position'
    form_class = forms.PositionForm
    deleter = utils.Deleter

class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'positions.delete_position'
    model = models.Position
    deleter = utils.Deleter