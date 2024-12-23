from django.views.generic import ListView, View, RedirectView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from . import models, forms, filters, mixins, resources, utils

from apps.base.utils.generic import OrderItem, OrderList
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
    
    permission_required = 'exchange_rates.view_exchangerate'
    sortable_by = OrderList([
        OrderItem(_('date'), 'date', checked=True),
        OrderItem(_('id'), 'pk', checked=True),
        OrderItem(_('currency'), 'currency__name'),
    ])
    filter_class = filters.ExchangeRateFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('exchange_rates:index'),
        'hx-target': '#exchange-rates-table #container > div',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'exchange_rates.can_export'
    resource_class = resources.ExchangeRateRecourse
    filter_class = filters.ExchangeRateFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'exchange_rates:bulk-delete',
        'bulk_reslugify': 'exchange_rates:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'exchange_rates.delete_exchangerate'
    model = models.ExchangeRate


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'exchange_rates.add_exchangerate'
    form_class = forms.ExchangeRateForm
    

class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View
):
    
    permission_required = 'exchange_rates.change_exchangerate'
    form_class = forms.ExchangeRateForm
    deleter = utils.Deleter


class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'exchange_rates.delete_exchangerate'
    model = models.ExchangeRate
    deleter = utils.Deleter