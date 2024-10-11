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
    
    model = models.City
    input_placeholder = _('search city')


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'cities.view_city'
    
    filter_class = filters.CityFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('cities:index'),
        'hx-target': '#cities-table #container > div',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'cities.can_export'
    resource_class = resources.CityRecourse
    filter_class = filters.CityFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'cities:bulk-delete',
        'bulk_reslugify': 'cities:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'cities:delete_city'
    model = models.City


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.City
    bulk_path = 'cities:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'cities.add_city'
    form_class = forms.CityForm


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View
):
    
    permission_required = 'cities.change_city'
    form_class = forms.CityForm
    deleter = utils.Deleter


class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'cities.delete_city'
    model = models.City
    deleter = utils.Deleter