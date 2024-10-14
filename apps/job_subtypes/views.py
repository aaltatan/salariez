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
    SearchMixin,
)


class SearchView(LoginRequiredMixin, SearchMixin, View):
    
    model = models.JobSubtype
    input_placeholder = _('search job subtype')


class ListTableView(
    LoginRequiredMixin, PermissionRequiredMixin, ListMixin, ListView
):
    
    permission_required = 'job_subtypes.view_jobsubtype'
    sortable_by = OrderList([
        OrderItem(_('job type'), 'job_type__name', checked=True),
        OrderItem(_('name'), 'name', checked=True),
        OrderItem(_('description'), 'description'),
    ])
    filter_class = filters.JobSubtypeFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('job_subtypes:index'),
        'hx-target': '#job-subtypes-table #container > div',
    }
    
    def get_queryset(self):
        return super().get_queryset().select_related('job_type')


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'job_subtypes.can_export'
    resource_class = resources.JobSubtypeRecourse
    filter_class = filters.JobSubtypeFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'job_subtypes:bulk-delete',
        'bulk_reslugify': 'job_subtypes:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'job_subtypes:delete_jobsubtype'
    model = models.JobSubtype


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.JobSubtype
    bulk_path = 'job_subtypes:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'job_subtypes.add_jobsubtype'
    form_class = forms.JobSubtypeForm
    

class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, View
):
    
    permission_required = 'job_subtypes.change_jobsubtype'
    form_class = forms.JobSubtypeForm
    deleter = utils.Deleter

class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'job_subtypes.delete_jobsubtype'
    model = models.JobSubtype
    deleter = utils.Deleter