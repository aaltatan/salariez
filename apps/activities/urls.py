from django.urls import path

from . import views

app_name = 'activities'

urlpatterns = [
  path(
    '<str:app_label>/<str:model_name>/<int:object_id>/', 
    views.ListView.as_view(),
    name='index'
  ),
]