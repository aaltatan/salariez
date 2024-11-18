from uuid import uuid4

from django.db.models import Model
from django.http import HttpRequest
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from djangoql.exceptions import (
    DjangoQLLexerError,
    DjangoQLParserError,
    DjangoQLSchemaError,
)
from djangoql.queryset import apply_search
from ninja import FilterSchema, Schema
from ninja_extra import status

from apps.base.utils.views import Deleter

from .schemas.utils import OrderBySchema, PaginationSchema


def get_list[T](
    model: type[Model],
    pagination: PaginationSchema,
    filters: FilterSchema,
    order_by: OrderBySchema[T],
    djangoql_filter: bool = True,
) -> dict:
    """
    Get a list of objects.
    """

    qs = model.objects.all()

    filtered_qs = filters.filter(qs)

    if djangoql_filter and getattr(filters, "djangoql", None):
        try:
            filtered_qs = apply_search(filtered_qs, getattr(filters, "djangoql", None))
        except (
            DjangoQLParserError,
            DjangoQLSchemaError,
            DjangoQLLexerError,
        ):
            filtered_qs = qs.none()

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


def create_objects(
    model: type[Model],
    data: list[Schema],
    slugify_field: str = "name",
    default_slug: None = None,
) -> tuple[int, dict]:
    """
    Create multiple objects.
    """
    default_slug = default_slug or uuid4().hex
    objs = [
        model(
            **m.model_dump(),
            slug=slugify(getattr(m, slugify_field, default_slug), allow_unicode=True),
        )
        for m in data
    ]
    objs = model.objects.bulk_create(objs)
    return status.HTTP_201_CREATED, {
        "status": status.HTTP_201_CREATED,
        "results": objs,
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


def delete_object(
    request: HttpRequest, model: type[Model], slug: str, deleter: Deleter
) -> tuple[int, dict]:
    """
    Delete an object.
    """
    obj = get_object_or_404(model, slug=slug)
    deleter = Deleter(obj, request, False, False)

    if not deleter.can_delete_condition():
        return status.HTTP_406_NOT_ACCEPTABLE, {"message": "object can't be deleted"}

    deleter.delete()

    return status.HTTP_204_NO_CONTENT, {
        "message": "object has been deleted successfully"
    }
