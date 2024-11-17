from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from ninja_extra import NinjaExtraAPI

from apps.base.views import logout_after_change_password

api = NinjaExtraAPI(
    title="Salariez API",
    description="Salariez API",
    urls_namespace="api",
    version="1.0.0",
    docs_decorator=login_required,
)

# register routers
api.add_router("cities/", "apps.api.routers.city.router")
api.add_router("areas/", "apps.api.routers.area.router")

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
    path("api/", api.urls),
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
