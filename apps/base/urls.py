from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
  path('', view=views.index, name='index'),
  path('messages/', view=views.get_messages, name='messages'),
  path('user-configurations/', view=views.user_configurations_modal, name='user-configurations'),
]
