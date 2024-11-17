from django.db.models import Model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import FilterSchema, Schema
from ninja_extra import status

from apps.base.utils.views import Deleter

from .schemas.utils import OrderBySchema, PaginationSchema


def get_list[T](
    model: type[Model],
    pagination: PaginationSchema,
    filters: FilterSchema,
    order_by: OrderBySchema[T],
) -> dict:
    """
    Get a list of objects.
    """

    qs = model.objects.all()

    filtered_qs = filters.filter(qs)

    qs = filtered_qs.order_by(*order_by.fields)[pagination.offset : pagination.limit]

    return {
        "total": filtered_qs.count(),
        "offset": pagination.offset,
        "limit": pagination.limit,
        "status": status.HTTP_200_OK,
        "results": qs,
    }


def create_object(model: type[Model], data: Schema) -> tuple[int, dict]:
    """
    Create a new object.
    """
    obj = model.objects.create(**data.model_dump())
    return status.HTTP_201_CREATED, {
        "status": status.HTTP_201_CREATED,
        "results": obj,
    }


def get_detail(model: type[Model], slug: str) -> dict:
    """
    Get a detail of an object.
    """
    obj = get_object_or_404(model, slug=slug)
    return {
        "status": status.HTTP_200_OK,
        "results": obj,
    }


# def update_object(model: type[Model], slug: str, data: PatchDict[Schema]) -> dict:
#     """
#     Update an object.
#     """
#     obj = get_object_or_404(model, slug=slug)
    
#     for k, v in data.items():
#         setattr(obj, k, v)

#     obj.save()

#     return {
#         "status": status.HTTP_202_ACCEPTED,
#         "results": obj,
#     }


def delete_object(
    request: HttpRequest, model: type[Model], slug: str, deleter: Deleter
) -> tuple[int, dict]:
    """
    Delete an object.
    """
    obj = get_object_or_404(model, slug=slug)
    deleter = Deleter(obj, request, False, False)

    if not deleter.can_delete_condition():
        return status.HTTP_406_NOT_ACCEPTABLE, {
            "message": "object can't be deleted"
        }
    
    deleter.delete()

    return status.HTTP_204_NO_CONTENT ,{
        "message": "object has been deleted successfully"
    }
