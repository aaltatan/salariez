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
    
    model = models.Nationality
    input_placeholder = _('search nationality')


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'nationalities.view_nationality'
    
    filter_class = filters.NationalityFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('nationalities:index'),
        'hx-target': '#nationalities-table',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'nationalities.can_export'
    resource_class = resources.NationalityRecourse
    filter_class = filters.NationalityFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'nationalities:bulk-delete',
        'bulk_reslugify': 'nationalities:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'nationalities:delete_nationality'
    model = models.Nationality


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.Nationality
    bulk_path = 'nationalities:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'nationalities.add_nationality'
    form_class = forms.NationalityForm


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View
):
    
    permission_required = 'nationalities.change_nationality'
    form_class = forms.NationalityForm
    deleter = utils.Deleter


class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'nationalities.delete_nationality'
    model = models.Nationality
    deleter = utils.Deleter