from django.urls import path

from .views import (
    ListTableView, 
    CreateView, 
    UpdateView,
    DeleteView, 
    BulkModalView,
    BulkDeleteView,
    ExportView,
)


app_name = 'exchange_rates'

urlpatterns = [
    path('', ListTableView.as_view(), name='index'),
    path('<int:id>/', ListTableView.as_view(), name='index'),
    path('create/', CreateView.as_view(), name='create'),
    path('bulk/', BulkModalView.as_view(), name='bulk'),
    path('export/', ExportView.as_view(), name='export'),
    path('bulk/delete/', BulkDeleteView.as_view(), name='bulk-delete'),
    path('update/<int:pk>/', UpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteView.as_view(), name='delete'),
]