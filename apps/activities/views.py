from django.http import HttpResponse, HttpRequest
from django.contrib.auth.mixins import (
  LoginRequiredMixin, PermissionRequiredMixin
)
from django.shortcuts import render
from django.views import View
from django.contrib.contenttypes.models import ContentType

from .models import Activity


class ListView(
  LoginRequiredMixin, PermissionRequiredMixin, View
):
    permission_required = 'activities.view_activity'
    model = Activity

    def get(
        self, 
        request: HttpRequest, 
        object_id: int, 
        app_label: str,
        model_name: str,
        *args, 
        **kwargs
    ) -> HttpResponse:
        
          content_type = ContentType.objects.get_by_natural_key(app_label, model_name)

          exec(f'from apps.{app_label}.models import {model_name}')
          instance = eval(f'{model_name}.objects.get(id={object_id})')

          qs = (
              self.model
              .objects.filter(content_type=content_type, object_id=object_id)
              .select_related('user')
          )

          context = {'qs': qs, 'instance': instance}
          
          return render(request, 'apps/activities/index.html', context)
