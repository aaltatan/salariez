from ninja_extra import NinjaExtraAPI

from .security import superuser_required


api = NinjaExtraAPI(
    title="Salariez API",
    description="Salariez API",
    urls_namespace="api",
    version="1.0.0",
    docs_decorator=superuser_required,
)

api.add_router("cities/", "apps.api.routers.city.router")
api.add_router("areas/", "apps.api.routers.area.router")