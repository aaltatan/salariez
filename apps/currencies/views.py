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
    
    permission_required = 'currencies.view_currency'
    sortable_by = OrderList([
        OrderItem(_('is local'), '-is_local', checked=True),
        OrderItem(_('name'), 'name', checked=True),
        OrderItem(_('fraction'), 'fraction_name'),
        OrderItem(_('short name'), 'short_name'),
        OrderItem(_('description'), 'description'),
    ])
    filter_class = filters.CurrencyFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('currencies:index'),
        'hx-target': '#currencies-table #container > div',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'currencies.can_export'
    resource_class = resources.CurrencyRecourse
    filter_class = filters.CurrencyFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'currencies:bulk-delete',
        'bulk_reslugify': 'currencies:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'currencies:delete_currency'
    model = models.Currency


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.Currency
    bulk_path = 'currencies:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'currencies.add_currency'
    form_class = forms.CurrencyForm


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View
):
    
    permission_required = 'currencies.change_currency'
    form_class = forms.CurrencyForm
    deleter = utils.Deleter


class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'currencies.delete_currency'
    model = models.Currency
    deleter = utils.Deleter