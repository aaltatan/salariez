from typing import Literal

from ninja import PatchDict, Query, Router
from ninja_extra import status

from apps.cities.models import City
from apps.cities.utils import Deleter

from .. import controllers
from ..schemas import city as schemas
from ..schemas import utils as utils_schemas
from ..security import PermissionAuth


router = Router(tags=["City"])

ORDER = Literal["id", "-id", "name", "-name", "description", "-description"]


@router.get(
    path="/",
    response=utils_schemas.ListWrapperSchema[list[schemas.CitySchema]],
    auth=PermissionAuth(perms=["cities.view_city"]),
)
def get_list(
    request,
    pagination: utils_schemas.PaginationSchema = Query(...),
    filter: schemas.CityFilterSchema = Query(...),
    order_by: utils_schemas.OrderBySchema[ORDER] = Query(...),
):
    return controllers.get_list(City, pagination, filter, order_by)


@router.post(
    path="/",
    response={
        status.HTTP_201_CREATED: utils_schemas.DetailWrapperSchema[schemas.CitySchema]
    },
    auth=PermissionAuth(perms=["cities.add_city"]),
)
def create_object(request, payload: schemas.CityCreateSchema):
    return controllers.create_object(City, payload)


@router.post(
    path="/bulk/",
    response={
        status.HTTP_201_CREATED: utils_schemas.BulkWrapperSchema[schemas.CitySchema]
    },
    auth=PermissionAuth(perms=["cities.add_city"]),
)
def create_objects(request, payload: list[schemas.CityCreateSchema]):
    return controllers.create_objects(City, payload)


@router.get(
    path="/{slug}",
    response=utils_schemas.DetailWrapperSchema[schemas.CitySchema],
    auth=PermissionAuth(perms=["cities.view_city"]),
)
def get_detail(request, slug: str):
    return controllers.get_detail(City, slug)


@router.put(
    path="/{slug}",
    response=utils_schemas.DetailWrapperSchema[schemas.CitySchema],
    auth=PermissionAuth(perms=["cities.change_city"]),
)
def update_object(request, payload: PatchDict[schemas.CityUpdateSchema], slug: str):
    return controllers.update_object(City, payload, slug)


@router.delete(
    path="/{slug}",
    response={
        status.HTTP_204_NO_CONTENT: utils_schemas.HttpError,
        status.HTTP_406_NOT_ACCEPTABLE: utils_schemas.HttpError,
    },
    auth=PermissionAuth(perms=["cities.delete_city"]),
)
def delete_object(request, slug: str):
    return controllers.delete_object(request, City, slug, Deleter)
