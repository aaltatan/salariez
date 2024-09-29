from django.urls import path

from . import views

app_name = 'departments'

urlpatterns = [
    path('', view=views.ListTableView.as_view(), name='index'),
    path('create/', view=views.CreateView.as_view(), name='create'),
    path('search/', view=views.SearchView.as_view(), name='search'),
    path('export/', view=views.ExportView.as_view(), name='export'),
    path('bulk/', view=views.BulkModalView.as_view(), name='bulk'),
    path('bulk/reslugify/', view=views.BulkReslugifyView.as_view(), name='bulk-reslugify'),
    path('delete/<str:slug>/', view=views.DeleteView.as_view(), name='delete'),
    path('update/<str:slug>/', view=views.UpdateView.as_view(), name='update'),
]