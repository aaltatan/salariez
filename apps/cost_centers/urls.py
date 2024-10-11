from django.urls import path

from .views import (
    ListTableView, 
    CreateView, 
    UpdateView,
    DeleteView, 
    BulkModalView,
    BulkDeleteView,
    BulkReslugifyView,
    SearchView,
    ExportView,
)


app_name = 'cost_centers'

urlpatterns = [
    path('', ListTableView.as_view(), name='index'),
    path('<int:id>/', ListTableView.as_view(), name='index'),
    path('create/', CreateView.as_view(), name='create'),
    path('bulk/', BulkModalView.as_view(), name='bulk'),
    path('search/', SearchView.as_view(), name='search'),
    path('export/', ExportView.as_view(), name='export'),
    path('bulk/delete/', BulkDeleteView.as_view(), name='bulk-delete'),
    path('bulk/reslugify/', BulkReslugifyView.as_view(), name='bulk-reslugify'),
    path('update/<str:slug>/', UpdateView.as_view(), name='update'),
    path('delete/<str:slug>/', DeleteView.as_view(), name='delete'),
]