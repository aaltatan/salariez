from django.urls import path

from . import views

app_name = 'departments'

urlpatterns = [
    path('', view=views.ListTableView.as_view(), name='index'),
    path('create/', view=views.CreateView.as_view(), name='create'),
    path('bulk-create/', view=views.BulkCreateView.as_view(), name='bulk-create'),
    path('search/', view=views.SearchView.as_view(), name='search'),
    path('empty/', view=views.EmptyView.as_view(), name='empty'),
    path('export/', view=views.ExportView.as_view(), name='export'),
    path('delete/<str:slug>/', view=views.DeleteView.as_view(), name='delete'),
    path('update/<str:slug>/', view=views.UpdateView.as_view(), name='update'),
]