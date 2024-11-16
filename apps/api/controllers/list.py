from django.db.models import Model
from ninja import FilterSchema
from ninja_extra import status

from ..schemas.utils import OrderBySchema, PaginationSchema


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
