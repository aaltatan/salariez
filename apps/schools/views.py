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
    
    permission_required = 'schools.view_school'
    sortable_by = OrderList([
        OrderItem(_('type'), 'school_type__name', checked=True),
        OrderItem(_('nationality'), '-nationality__is_local', checked=True),
        OrderItem(_('nationality name'), 'nationality__name', checked=True),
        OrderItem(_('name'), 'name', checked=True),
        OrderItem(_('description'), 'description'),
    ])
    filter_class = filters.SchoolFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('schools:index'),
        'hx-target': '#schools-table #container > div',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'schools.can_export'
    resource_class = resources.SchoolRecourse
    filter_class = filters.SchoolFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'schools:bulk-delete',
        'bulk_reslugify': 'schools:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'schools.delete_school'
    model = models.School


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.School
    bulk_path = 'schools:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'schools.add_school'
    form_class = forms.SchoolForm


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin,View
):
    
    permission_required = 'schools.change_school'
    form_class = forms.SchoolForm
    deleter = utils.Deleter

class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'schools.delete_school'
    model = models.School
    deleter = utils.Deleter