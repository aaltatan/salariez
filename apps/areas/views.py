from django.views.generic import ListView, View, RedirectView
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from braces.views import SuperuserRequiredMixin

from . import models, forms, filters, mixins, resources

from apps.base import forms as base_forms
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
    
    model = models.Area
    input_placeholder = _('search area')


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'areas.view_area'
    
    model = models.Area
    filter_class = filters.AreaFilterSet
    
    template_name = 'apps/areas/partials/table.html'
    index_template_name = 'apps/areas/index.html'
    
    paginate_by_form = base_forms.PaginatedByForm
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('areas:index'),
        'hx-target': '#areas-table',
    }

    def get_queryset(self):
        return super().get_queryset().select_related('city')


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'areas.can_export'
    resource_class = resources.AreaRecourse
    filter_class = filters.AreaFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'areas:bulk-delete',
        'bulk_reslugify': 'areas:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'areas:delete_area'
    model = models.Area


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.Area
    bulk_path = 'areas:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'areas.add_area'
    form_class = forms.AreaForm
    

class UpdateView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    UpdateMixin,
    mixins.CannotDeleteMixin, 
    View
):
    
    permission_required = 'areas.change_area'
    form_class = forms.AreaForm


class DeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    DeleteMixin, 
    mixins.CannotDeleteMixin, 
    View
):

    permission_required = 'areas.delete_area'
    model = models.Area
