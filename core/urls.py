from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from apps.base.views import logout_after_change_password


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("password-change-done/", logout_after_change_password, name='password_change_done'),
    # apps
    path('', include('apps.base.urls')),
    path('faculties/', include('apps.faculties.urls')),
    path('job-types/', include('apps.job_types.urls')),
    path('job-subtypes/', include('apps.job_subtypes.urls')),
    path('departments/', include('apps.departments.urls')),
    path('positions/', include('apps.positions.urls')),
]

if settings.DEBUG:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]