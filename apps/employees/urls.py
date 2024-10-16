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
    EmployeeDetailView,
    # formsets
    MobileFormSetView,
    EmailFormSetView,
    PhoneFormSetView,
    EducationalTransactionFormSetView,
    # dashboard
    male_female_card,
)


app_name = 'employees'

urlpatterns = [
    path('', ListTableView.as_view(), name='index'),
    path('<int:id>/', ListTableView.as_view(), name='index'),
    path('create/', CreateView.as_view(), name='create'),
    path('bulk/', BulkModalView.as_view(), name='bulk'),
    path('search/', SearchView.as_view(), name='search'),
    path('export/', ExportView.as_view(), name='export'),
    path('bulk/delete/', BulkDeleteView.as_view(), name='bulk-delete'),
    path('bulk/reslugify/', BulkReslugifyView.as_view(), name='bulk-reslugify'),
    path('details/<str:slug>/', EmployeeDetailView.as_view(), name='details'),
    path('delete/<str:slug>/', DeleteView.as_view(), name='delete'),
    path('update/<str:slug>/', UpdateView.as_view(), name='update'),
    # formsets
    path('update/<str:slug>/mobiles/', MobileFormSetView.as_view(), name='update-mobiles'),
    path('update/<str:slug>/emails/', EmailFormSetView.as_view(), name='update-emails'),
    path('update/<str:slug>/phones/', PhoneFormSetView.as_view(), name='update-phones'),
    path('update/<str:slug>/educational-transactions/', EducationalTransactionFormSetView.as_view(), name='update-educational-transactions'),
    # dashboard
    path('dashboard/male-female-counts/', male_female_card, name='dashboard-male-female')
]