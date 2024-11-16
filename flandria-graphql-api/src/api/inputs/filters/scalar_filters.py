from typing import Generic, TypeVar

import strawberry

T = TypeVar("T")


class ScalarFilter:
    pass


@strawberry.input(one_of=True)
class BooleanFilter(ScalarFilter):
    eq: bool | None = strawberry.UNSET


@strawberry.input(one_of=True)
class StringFilter(ScalarFilter):
    eq: str | None = strawberry.UNSET
    ne: str | None = strawberry.UNSET

    in_: list[str] | None = strawberry.field(name="in", default=strawberry.UNSET)

    like: str | None = strawberry.UNSET
    ilike: str | None = strawberry.UNSET


@strawberry.input(one_of=True)
class NumberFilter(ScalarFilter):
    eq: int | None = strawberry.UNSET
    ne: int | None = strawberry.UNSET
    in_: list[int] | None = strawberry.field(name="in", default=strawberry.UNSET)
    gt: int | None = strawberry.UNSET
    ge: int | None = strawberry.UNSET
    lt: int | None = strawberry.UNSET
    le: int | None = strawberry.UNSET
    between: list[int] | None = strawberry.field(
        default=strawberry.UNSET,
        description="Only the first two numbers are considered",
    )


@strawberry.input(one_of=True)
class EnumFilter(ScalarFilter, Generic[T]):
    eq: T | None = strawberry.UNSET
    ne: T | None = strawberry.UNSET
    in_: list[T] | None = strawberry.field(name="in", default=strawberry.UNSET)
