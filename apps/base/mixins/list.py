from typing import Any, Literal
from abc import ABC, abstractmethod

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.urls import reverse

from .utils import HelperMixin


PERMS = Literal['create', 'update', 'delete', 'export', 'log']


class AbstractList(ABC):
    
    @property
    @abstractmethod
    def model(self): ...
    
    @property
    @abstractmethod
    def filter_class(self): ...
    
    @property
    @abstractmethod
    def template_name(self): ...
    
    @property
    @abstractmethod
    def paginate_by_form(self): ...
    
    @property
    @abstractmethod
    def paginate_by_form_attributes(self): ...
    
    
class ListMixin(HelperMixin, AbstractList):
    
    """
    utility class to implement list(table) view and its functionality.  
    
    ### required attributes:  
    - `model: Model`
    - `filter_class: FilterSet`
    - `template_name: str` table template path like `apps/<app_name>/partials/table.html`
    - `paginate_by_form: Form`
    - `paginate_by_form_attributes: dict[str, reverse_lazy | str]` to set hx-get and hx-target attrs on form attributes  

    ### optional attributes:  
    - `filter_form_id: str` like `<app_name>-filter-form`
    
    # Note:  
    and also you need to implement `get_delete_path`, `get_delete_path` and `get_create_path` in the model which you will use in the view.
    """
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        for property in ['get_delete_path', 'get_update_path']:
            if not hasattr(self.model, property):
                model_name = self.model._meta.model_name.title()
                raise NotImplementedError(
                    f'you implement {property} property on {model_name} model'
                )
        
        context = self.get_context_data()
        response = render(request, self.template_name, context)
        response['Hx-Trigger'] = 'get-messages'
        return response

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        append `qs`, `filter_form` and `pagination_form` to the context
        """
        context = super().get_context_data(
            object_list=self.get_queryset(), **kwargs
        )

        app_label = self._get_app_label()

        context = {
            **context,
            'filter': self.filter_class(self.request.GET).form, 
            'qs': self.get_paginator_queryset(),
            'pagination_form': self.get_pagination_form(),
            ######
            'index_path': reverse(f'{app_label}:index'),
            'bulk_path': reverse(f'{app_label}:bulk'),
            'create_path': reverse(f'{app_label}:create'),
            'export_path': reverse(f'{app_label}:export'),
            ######
            'can_create': self._has_perm('create'),
            'can_delete': self._has_perm('delete'),
            'can_update': self._has_perm('update'),
            'can_export': self._has_perm('export'),
            'can_log': self._has_perm('log'),
            ######
            'target': self.paginate_by_form_attributes['hx-target'],
            'filter_form': self._get_filter_form_id()
        }
        
        return context
    
    def _get_filter_form_id(self):

        if getattr(self, 'filter_form_id', None) is not None:
            return self.filter_form_id

        app_label = self._get_app_label()
        return f'{app_label}-filter-form'

    def _has_perm(self, perm: PERMS) -> bool:

        request: HttpRequest = self.request
        app_label = self._get_app_label()
        object_name = self._get_object_name()

        perms = {
            'create': f'{app_label}.create_{object_name}',
            'update': f'{app_label}.change_{object_name}',
            'delete': f'{app_label}.delete_{object_name}',
            'export': 'can_export',
            'log': 'can_log',
        }

        perm = perms[perm]

        return request.user.has_perm(f'{app_label}.{perm}')

    def get_paginator_queryset(self):
        
        qs = self.get_queryset()
        paginate_by = self.get_paginate_by(qs)
        paginator: Paginator = self.get_paginator(qs, paginate_by)
        page = self.get_current_page()
        
        return paginator.get_page(page).object_list

    def get_queryset(self):
        """
        filtering the queryset by filter_class
        """
        
        default_ordering = self._get_default_ordering()
        request_ordering = self.request.GET.get('order')
        
        order = default_ordering
        
        if request_ordering is not None and request_ordering != '':
            order = [request_ordering]

        qs: QuerySet = (
            self
            .filter_class(self.request.GET or self.request.POST)
            .qs
            .order_by(*order)
        )
        return qs
    
    def get_current_page(self) -> int:
        return int(self.request.GET.get('page', 1))
    
    def paginate_queryset(self, queryset, page_size):
        paginator: Paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        
        page = self.get_current_page()
        
        if paginator.num_pages < page:
            page = paginator.num_pages
        
        page = paginator.page(page)
        return paginator, page, page.object_list, page.has_other_pages()
    
    def get_pagination_form(self):

        attrs = self.paginate_by_form_attributes
        attrs['hx-select'] = attrs['hx-target']
        
        pagination_form = self.paginate_by_form(
            data=self.request.GET, attrs=attrs
        )
        return pagination_form
    
    def get_paginate_by(self, queryset) -> int | None:
        
        pagination_form = self.get_pagination_form()
        
        per_page = self.paginate_by_form.PaginationChoices.TEN
            
        if pagination_form.data.get('per_page'):
            per_page = pagination_form.data.get('per_page')
        
        if pagination_form.data.get('per_page') == 'all':
            per_page = 1_000_000_000
        
        return int(per_page)