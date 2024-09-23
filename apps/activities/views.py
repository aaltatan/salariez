from django.shortcuts import get_list_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.mixins import (
  LoginRequiredMixin, PermissionRequiredMixin
)
from django.views import View

from .models import Activity


class ListView(
  LoginRequiredMixin, PermissionRequiredMixin, View
):
    permission_required = 'activities.view_activity'
    model = Activity

    def get_queryset(self):
        return self.model.objects.all()

    def get(
        self, 
        request: HttpRequest, 
        object_id: int, 
        app_label: str,
        *args, 
        **kwargs
    ) -> HttpResponse:
        
        qs = get_list_or_404(self.model, kwargs={'id': id})
