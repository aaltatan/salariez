from django.views.generic import ListView, View, RedirectView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from . import models, forms, filters, mixins, resources

from apps.base import forms as base_forms
from apps.base.mixins import (
    ListMixin,
    CreateMixin,
    UpdateMixin,
    DeleteMixin,
    BulkModalMixin,
    BulkMapperMixin,
    SearchMixin,
    ExportMixin,
)


class SearchView(LoginRequiredMixin, SearchMixin, View):
    
    model = models.CostCenter
    input_placeholder = _('search cost center')
    search_container_id = 'cost-center-search-container'


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'cost_centers.view_cost_center'
    
    model = models.CostCenter
    filter_class = filters.CostCenterFilterSet
    
    template_name = 'apps/cost_centers/partials/table.html'
    index_template_name = 'apps/cost_centers/index.html'
    
    paginate_by_form = base_forms.PaginatedByForm
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('cost_centers:index'),
        'hx-target': '#cost-centers-table',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'cost_centers.can_export'
    resource_class = resources.CostCenterRecourse
    filter_class = filters.CostCenterFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'cost_centers:bulk-delete'
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'cost_centers:delete_cost_center'
    model = models.CostCenter
    hx_location_target = '#cost-centers-table'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'cost_centers.add_cost_center'
    form_class = forms.CostCenterForm
    template_name = 'apps/cost_centers/create.html'
    

class UpdateView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    UpdateMixin, 
    mixins.CannotDeleteMixin, 
    View
):
    
    permission_required = 'cost_centers.change_cost_center'
    form_class = forms.CostCenterForm
    template_name = 'apps/cost_centers/update.html'


class DeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    DeleteMixin, 
    mixins.CannotDeleteMixin, 
    View
):

    permission_required = 'cost_centers.delete_cost_center'
    model = models.CostCenter
    hx_location_target = '#cost-centers-table'