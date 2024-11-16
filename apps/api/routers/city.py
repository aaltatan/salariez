from typing import Literal

from ninja import Query, Router

from apps.cities.models import City

from .. import controllers
from ..schemas import city as schemas
from ..schemas import utils as utils_schemas

router = Router(tags=["City"])

ORDER = Literal["id", "-id", "name", "-name", "description", "-description"]


@router.get(
    "/",
    response=utils_schemas.ListWrapperSchema[list[schemas.CitySchema]],
)
def get_cities(
    request,
    pagination: utils_schemas.PaginationSchema = Query(...),
    filter: schemas.CityFilterSchema = Query(...),
    order_by: utils_schemas.OrderBySchema[ORDER] = Query(...),
):
    return controllers.get_list(City, pagination, filter, order_by)
