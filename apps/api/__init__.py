from rest_framework import routers

from apps.areas.api import AreaViewSet
from apps.cities.api import CityViewSet
from apps.cost_centers.api import CostCenterViewSet
from apps.currencies.api import CurrencyViewSet
from apps.departments.api import DepartmentViewSet
from apps.educational_degrees.api import EducationalDegreeViewSet
from apps.employees.api import EmployeeViewSet
from apps.exchange_rates.api import ExchangeRateViewSet
from apps.groups.api import GroupViewSet
from apps.job_subtypes.api import JobSubtypeViewSet
from apps.job_types.api import JobTypeViewSet
from apps.nationalities.api import NationalityViewSet
from apps.positions.api import PositionViewSet
from apps.school_types.api import SchoolTypeViewSet
from apps.schools.api import SchoolViewSet
from apps.specializations.api import SpecializationViewSet
from apps.statuses.api import StatusViewSet


router = routers.DefaultRouter()

# register viewsets
router.register(r"areas", AreaViewSet)
router.register(r"cities", CityViewSet)
router.register(r"cost-centers", CostCenterViewSet)
router.register(r"currencies", CurrencyViewSet)
router.register(r"departments", DepartmentViewSet)
router.register(r"educational-degrees", EducationalDegreeViewSet)
router.register(r"employees", EmployeeViewSet)
router.register(r"exchange-rates", ExchangeRateViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"job-subtypes", JobSubtypeViewSet)
router.register(r"job-types", JobTypeViewSet)
router.register(r"nationalities", NationalityViewSet)
router.register(r"positions", PositionViewSet)
router.register(r"school-types", SchoolTypeViewSet)
router.register(r"schools", SchoolViewSet)
router.register(r"specializations", SpecializationViewSet)
router.register(r"statuses", StatusViewSet)