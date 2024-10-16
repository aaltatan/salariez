from .crud import (
  ListTableView,
  BulkModalView,
  BulkDeleteView,
  BulkMapperMixin,
  CreateView,
  DeleteView,
  ExportView,
  UpdateView,
  BulkReslugifyView,
  SearchView,
  EmployeeDetailView,
)
from .formsets import (
  MobileFormSetView,
  EmailFormSetView,
  PhoneFormSetView,
  EducationalTransactionFormSetView,
)
from .dashboard import (
  male_female_card,
)

__all__ = [
  ListTableView,
  BulkModalView,
  BulkDeleteView,
  BulkMapperMixin,
  CreateView,
  DeleteView,
  ExportView,
  BulkReslugifyView,
  SearchView,
  UpdateView,
  EmployeeDetailView,
  # formsets
  MobileFormSetView,
  EmailFormSetView,
  PhoneFormSetView,
  EducationalTransactionFormSetView,
  # dashboard
  male_female_card,
]