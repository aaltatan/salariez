from typing import Literal

from ninja import Query, Router

from apps.areas.models import Area

from .. import controllers
from ..schemas import area as schemas
from ..schemas import utils as utils_schemas

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
)
def get_cities(
    request,
    pagination: utils_schemas.PaginationSchema = Query(...),
    filter: schemas.AreaFilterSchema = Query(...),
    order_by: utils_schemas.OrderBySchema[ORDER] = Query(...),
):
    return controllers.get_list(Area, pagination, filter, order_by)
