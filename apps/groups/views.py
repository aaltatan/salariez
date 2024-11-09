from django.views.generic import ListView, View, RedirectView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from braces.views import SuperuserRequiredMixin

from . import models, forms, filters, mixins, resources, utils

from apps.base.utils.generic import OrderItem, OrderList
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
    
    permission_required = 'groups.view_group'
    sortable_by = OrderList([
        OrderItem(_('name'), 'name', checked=True),
        OrderItem(_('description'), 'description'),
    ])
    filter_class = filters.GroupFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('groups:index'),
        'hx-target': '#groups-table #container > div',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'groups.can_export'
    resource_class = resources.GroupRecourse
    filter_class = filters.GroupFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'groups:bulk-delete',
        'bulk_reslugify': 'groups:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'groups.delete_group'
    model = models.Group


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.Group
    bulk_path = 'groups:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'groups.add_group'
    form_class = forms.GroupForm


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin,View
):
    
    permission_required = 'groups.change_group'
    form_class = forms.GroupForm
    deleter = utils.Deleter

class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'groups.delete_group'
    model = models.Group
    deleter = utils.Deleter