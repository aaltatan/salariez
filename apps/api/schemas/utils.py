from ninja import Schema


class HttpError(Schema):
    message: str


class PaginationSchema(Schema):
    offset: int = 0
    limit: int = 10


class OrderBySchema[T](Schema):
    fields: list[T] = []


class ListWrapperSchema[T](Schema):
    status: int
    total: int
    offset: int
    limit: int
    results: T


class DetailWrapperSchema[T](Schema):
    status: int
    results: T
