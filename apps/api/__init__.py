from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from .security import superuser_required


api = NinjaExtraAPI(
    title="Salariez API",
    description="Salariez API",
    urls_namespace="api",
    version="1.0.0",
    docs_decorator=superuser_required,
    csrf=True,
)

api.register_controllers(NinjaJWTDefaultController)

api.add_router("cities/", "apps.api.routers.city.router")
api.add_router("areas/", "apps.api.routers.area.router")