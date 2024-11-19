from typing import Literal

from ninja import Query, Router
from ninja_extra import status

from apps.areas.models import Area

from .. import controllers
from ..schemas import area as schemas
from ..schemas import utils as utils_schemas
from ..security import PermissionAuth

router = Router(tags=["Area"])

ORDER = Literal[
    "id",
    "-id",
    "name",
    "-name",
    "city__name",
    "-city__name",
    "city__description",
    "-city__description",
    "description",
    "-description",
]


@router.get(
    "/",
    response=utils_schemas.ListWrapperSchema[list[schemas.AreaSchema]],
    auth=PermissionAuth(perms=["areas.view_area"]),
)
def get_list(
    request,
    pagination: utils_schemas.PaginationSchema = Query(...),
    filter: schemas.AreaFilterSchema = Query(...),
    order_by: utils_schemas.OrderBySchema[ORDER] = Query(...),
):
    return controllers.get_list(Area, pagination, filter, order_by)


@router.post(
    "/",
    response={
        status.HTTP_201_CREATED: utils_schemas.DetailWrapperSchema[schemas.AreaSchema],
    },
    auth=PermissionAuth(perms=["areas.add_area"]),
)
def create_object(request, payload: schemas.AreaCreateSchema):
    return controllers.create_object(Area, payload)
