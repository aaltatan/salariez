from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.base.views import logout_after_change_password

# viewsets
from apps.cities.api import CityViewSet
from apps.areas.api import AreaViewSet

router = DefaultRouter()
router.register(r"cities", CityViewSet)
router.register(r"areas", AreaViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "password-change-done/",
        logout_after_change_password,
        name="password_change_done",
    ),
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
