from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.base.views import logout_after_change_password

# viewsets
from apps.areas.api import AreaViewSet
from apps.cities.api import CityViewSet
from apps.cost_centers.api import CostCenterViewSet
from apps.educational_degrees.api import EducationalDegreeViewSet
from apps.groups.api import GroupViewSet
from apps.job_types.api import JobTypeViewSet
from apps.job_subtypes.api import JobSubtypeViewSet
from apps.nationalities.api import NationalityViewSet
from apps.positions.api import PositionViewSet
from apps.school_types.api import SchoolTypeViewSet
from apps.schools.api import SchoolViewSet
from apps.specializations.api import SpecializationViewSet
from apps.statuses.api import StatusViewSet
from apps.currencies.api import CurrencyViewSet
from apps.exchange_rates.api import ExchangeRateViewSet
from apps.departments.api import DepartmentViewSet
from apps.employees.api import EmployeeViewSet


router = DefaultRouter()

router.register(r"cities", CityViewSet)
router.register(r"areas", AreaViewSet)
router.register(r"cost-centers", CostCenterViewSet)
router.register(r"educational-degrees", EducationalDegreeViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"job-types", JobTypeViewSet)
router.register(r"job-subtypes", JobSubtypeViewSet)
router.register(r"positions", PositionViewSet)
router.register(r"nationalities", NationalityViewSet)
router.register(r"school-types", SchoolTypeViewSet)
router.register(r"schools", SchoolViewSet)
router.register(r"specializations", SpecializationViewSet)
router.register(r"statuses", StatusViewSet)
router.register(r"currencies", CurrencyViewSet)
router.register(r"exchange-rates", ExchangeRateViewSet)
router.register(r"departments", DepartmentViewSet)
router.register(r"employees", EmployeeViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "password-change-done/",
        logout_after_change_password,
        name="password_change_done",
    ),
    # api
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # apps
    path("", include("apps.base.urls")),
    path("job-types/", include("apps.job_types.urls")),
    path("job-subtypes/", include("apps.job_subtypes.urls")),
    path("cost-centers/", include("apps.cost_centers.urls")),
    path("departments/", include("apps.departments.urls")),
    path("positions/", include("apps.positions.urls")),
    path("cities/", include("apps.cities.urls")),
    path("areas/", include("apps.areas.urls")),
    path("nationalities/", include("apps.nationalities.urls")),
    path("statuses/", include("apps.statuses.urls")),
    path("activities/", include("apps.activities.urls")),
    ####################
    path("currencies/", include("apps.currencies.urls")),
    path("exchange-rates/", include("apps.exchange_rates.urls")),
    ####################
    path("specializations/", include("apps.specializations.urls")),
    path("educational-degrees/", include("apps.educational_degrees.urls")),
    path("school-types/", include("apps.school_types.urls")),
    path("schools/", include("apps.schools.urls")),
    ####################
    path("employees/", include("apps.employees.urls")),
    path("groups/", include("apps.groups.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
