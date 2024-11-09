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
    
    permission_required = 'school_types.view_schooltype'
    sortable_by = OrderList([
        OrderItem(_('name'), 'name', checked=True),
        OrderItem(_('description'), 'description'),
    ])
    filter_class = filters.SchoolTypeFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('school_types:index'),
        'hx-target': '#school-types-table #container > div',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'school_types.can_export'
    resource_class = resources.SchoolTypeRecourse
    filter_class = filters.SchoolTypeFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'school_types:bulk-delete',
        'bulk_reslugify': 'school_types:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'school_types.delete_schooltype'
    model = models.SchoolType


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.SchoolType
    bulk_path = 'school_types:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'school_types.add_schooltype'
    form_class = forms.SchoolTypeForm


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin,View
):
    
    permission_required = 'school_types.change_schooltype'
    form_class = forms.SchoolTypeForm
    deleter = utils.Deleter

class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'school_types.delete_schooltype'
    model = models.SchoolType
    deleter = utils.Deleter