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
    
    permission_required = 'educational_degrees.view_educationaldegree'
    sortable_by = OrderList([
        OrderItem(_('order'), 'order', checked=True),
        OrderItem(_('is academic'), '-is_academic', checked=True),
        OrderItem(_('name'), 'name'),
        OrderItem(_('description'), 'description'),
    ])
    filter_class = filters.EducationalDegreeFilterSet
    paginate_by_form_attributes = {
        'hx-get': reverse_lazy('educational_degrees:index'),
        'hx-target': '#educational-degrees-table #container > div',
    }


class ExportView(
    LoginRequiredMixin, PermissionRequiredMixin, ExportMixin, View
):
    
    permission_required = 'educational_degrees.can_export'
    resource_class = resources.EducationalDegreeRecourse
    filter_class = filters.EducationalDegreeFilterSet


class BulkModalView(LoginRequiredMixin, BulkMapperMixin, RedirectView):
    
    mapper = {
        'bulk_delete': 'educational_degrees:bulk-delete',
        'bulk_reslugify': 'educational_degrees:bulk-reslugify',
    }


class BulkDeleteView(
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    BulkModalMixin,
    mixins.BulkDeleteMixin, # local mixins 
    View
):
    
    permission_required = 'educational_degrees:delete_educationaldegree'
    model = models.EducationalDegree


class BulkReslugifyView(
    LoginRequiredMixin, 
    BulkModalMixin,
    SuperuserRequiredMixin,
    ReslugifyModalMixin,
    View
):
    model = models.EducationalDegree
    bulk_path = 'educational_degrees:bulk-reslugify'


class CreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateMixin, View
):
    
    permission_required = 'educational_degrees.add_educationaldegree'
    form_class = forms.EducationalDegreeForm


class UpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin,View
):
    
    permission_required = 'educational_degrees.change_educationaldegree'
    form_class = forms.EducationalDegreeForm
    deleter = utils.Deleter

class DeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, View
):

    permission_required = 'educational_degrees.delete_educationaldegree'
    model = models.EducationalDegree
    deleter = utils.Deleter