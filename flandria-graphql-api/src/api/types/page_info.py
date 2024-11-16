import strawberry


@strawberry.type
class PageInfo[T]:
    offset: int
    limit: int
    count: int
    total_count: int
    items: list[T]
