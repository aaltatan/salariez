from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
  path('', view=views.index, name='index'),
  path('messages/', view=views.get_messages, name='messages'),
  # fields
  path('fields/avatar/<str:id>/<str:name>', view=views.get_avatar_field, name='fields-avatar'),
]
