from typing import Literal

from django.shortcuts import get_object_or_404
from ninja import Query, Router
from ninja_extra import status

from apps.cities.models import City
from apps.cities.utils import Deleter

from .. import controllers
from ..schemas import city as schemas
from ..schemas import utils as utils_schemas
from ..security import Permission, PermissionAuth


router = Router(tags=["City"])

ORDER = Literal["id", "-id", "name", "-name", "description", "-description"]


@router.get(
    path="/",
    response=utils_schemas.ListWrapperSchema[list[schemas.CitySchema]],
    auth=PermissionAuth(perms=[Permission("cities", "city", "view")]),
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
)
def create_object(request, payload: schemas.CityCreateSchema):
    return controllers.create_object(City, payload)


@router.post(
    path="/bulk/",
    response={
        status.HTTP_201_CREATED: utils_schemas.BulkWrapperSchema[schemas.CitySchema]
    },
)
def create_objects(request, payload: list[schemas.CityCreateSchema]):
    return controllers.create_objects(City, payload)


@router.get(
    path="/{slug}", response=utils_schemas.DetailWrapperSchema[schemas.CitySchema]
)
def get_detail(request, slug: str):
    return controllers.get_detail(City, slug)


@router.delete(
    path="/{slug}",
    response={
        status.HTTP_204_NO_CONTENT: utils_schemas.HttpError,
        status.HTTP_406_NOT_ACCEPTABLE: utils_schemas.HttpError,
    },
)
def delete_object(request, slug: str):
    obj = get_object_or_404(City, slug=slug)
    deleter = Deleter(obj, request, False, False)

    if deleter.can_delete_condition():
        deleter.delete()
    else:
        return status.HTTP_406_NOT_ACCEPTABLE, {"message": "object can't be deleted"}

    return status.HTTP_204_NO_CONTENT, {
        "message": "object has been deleted successfully"
    }
