from typing import Any
from abc import ABC, abstractmethod

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
from django.urls import reverse

from .utils import HelperMixin
from ..utils.generic import OrderItem, OrderList

from apps.base import forms as base_forms



class AbstractList(ABC):
    
    @property
    @abstractmethod
    def filter_class(self): ...
    
    @property
    @abstractmethod
    def sortable_by(self) -> OrderList: ...
    
    @property
    @abstractmethod
    def paginate_by_form_attributes(self): ...
    
    
class ListMixin(HelperMixin, AbstractList):
    """
    utility class to implement list(table) view and its functionality.  
    
    ### required attributes:  
    - `filter_class: FilterSet`
    - `sortable_by: OrderList` to use it in order functionality, it must be `OrderList` which contains `OrderItem` objects.  
    - `paginate_by_form_attributes: dict[str, reverse_lazy | str]` to set hx-get and hx-target attrs on form attributes  

    ### optional attributes:  
    - `model: Model`
    - `template_name: str` table template path like `apps/<app_name>/partials/table.html`
    - `filter_form_id: str` like `<app_name>-filter-form`
    - `paginate_by_form: Form`
    
    # Note:  
    and also you need to implement `get_delete_path`, `get_delete_path` and `get_create_path` in the model which you will use in the view.
    """
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        model = self._get_model_class()

        for property in ['get_delete_path', 'get_update_path']:
            if not hasattr(model, property):
                model_name = model._meta.model_name.title()
                raise NotImplementedError(
                    f'you implement {property} property on {model_name} model'
                )
            
        template_name = self.get_template_name()
        if request.headers.get('partial'):
            template_name = self.get_partial_template_name()
        
        context = self.get_context_data()
        response = render(request, template_name, context)
        response['Hx-Trigger'] = 'get-messages'
        return response
    
    def get_template_name(self) -> str:

        if getattr(self, 'template_name', None) is not None:
            return self.template_name
        
        app_label = self._get_app_label()
        return f'apps/{app_label}/index.html'
    
    def get_partial_template_name(self) -> str:

        if getattr(self, 'partial_template_name', None) is not None:
            return self.partial_template_name
        
        app_label = self._get_app_label()
        return f'apps/{app_label}/partials/index/table.html'

    def get_context_data(
        self, **kwargs: Any
    ) -> dict[str, Any]:
        """
        append `qs`, `filter_form` and `pagination_form` to the context
        """
        
        context = super().get_context_data(
            object_list=self.get_queryset(), **kwargs
        )
        request: HttpRequest = self.request

        app_label = self._get_app_label()

        context = {
            **context,
            'filter': self.filter_class(request.GET).form, 
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
            'can_activity': request.user.has_perm('activities.view_activity'),
            ######
            'ordering': self.get_ordering().get_order_json() ,
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

    def get_paginator_queryset(self):
        
        qs = self.get_queryset()
        paginate_by = self.get_paginate_by(qs)
        paginator: Paginator = self.get_paginator(qs, paginate_by)
        page = self.get_current_page()
        
        return paginator.get_page(page).object_list
    
    def normalize_sort_item(self, string: str) -> str:
        return string[1:] if string.startswith('-') else string 
    
    def normalize_sort_list(self, lst: list[str]) -> list[str]:
        return [
            self.normalize_sort_item(o) for o in lst
        ]
    
    def get_ordering(self) -> OrderList:

        request_order: list = self.request.GET.getlist('order')
        sortable_by: OrderList = self.sortable_by

        if not any(request_order):
            return sortable_by
        
        order_list: list = []

        for request_item in request_order:
            for sort_item in sortable_by.order_list:
                if sort_item == request_item:
                    order_list.append(OrderItem(
                        name=sort_item.name, 
                        code=request_item, 
                        checked=True
                    ))

        normalized_request_list = self.normalize_sort_list(
            request_order
        )

        for sort_item in sortable_by.order_list:
            if sort_item.normalize_name not in normalized_request_list:
                order_list.append(OrderItem(
                    name=sort_item.name, 
                    code=sort_item.code, 
                ))

        return OrderList(order_list)

    def get_queryset(self):
        """
        filtering the queryset by filter_class
        """
        return (
            self
            .filter_class(self.request.GET or self.request.POST)
            .qs
            .order_by(*self.get_ordering().get_order_list())
        )
    
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

        if getattr(self, 'paginate_by_form', None) is not None:
            paginate_by_form = self.paginate_by_form
        else:
            paginate_by_form = base_forms.PaginatedByForm

        attrs = self.paginate_by_form_attributes
        
        pagination_form = paginate_by_form(
            data=self.request.GET, attrs=attrs
        )
        return pagination_form
    
    def get_paginate_by(self, queryset) -> int | None:
        
        pagination_form = self.get_pagination_form()
        
        per_page = pagination_form.PaginationChoices.TEN
            
        if pagination_form.data.get('per_page'):
            per_page = pagination_form.data.get('per_page')
        
        if pagination_form.data.get('per_page') == 'all':
            per_page = 1_000_000_000
        
        return int(per_page)