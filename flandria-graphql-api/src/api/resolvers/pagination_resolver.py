from dataclasses import Field
from typing import TYPE_CHECKING, Any, ClassVar, Protocol, Type, TypeVar

import sqlalchemy as sa
import strawberry

from src.api.types import PageInfo
from src.database import Session

from .helpers import coerce_orm_to_strawberry, parse_nested_keys_from_selections
from .sqla_helpers import apply_filters, apply_join_options, apply_order_by

if TYPE_CHECKING:
    from src.database.types import ModelCls

T = TypeVar("T")


class Filter(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


class OrderBy(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


def resolve_pagination(
    *,
    info: strawberry.Info,
    model_cls: "ModelCls",
    object_cls: Type[T],
    limit: int,
    offset: int,
    filter: "Filter | None" = None,
    order_by: "list[OrderBy] | None" = None,
) -> PageInfo[T]:
    nested_keys = parse_nested_keys_from_selections(info.selected_fields)
    # our actual keys for the model are always inside <query name> -> <items> -> ...
    nested_keys = nested_keys[info._raw_info.field_name]["items"]

    query = sa.select(model_cls)

    if nested_keys:
        query = apply_join_options(query, model_cls, nested_keys)

    if not (filter is None or filter is strawberry.UNSET):
        query = apply_filters(query, model_cls, filter)

    if not (order_by is None or not order_by or order_by is strawberry.UNSET):
        query = apply_order_by(query, model_cls, order_by)

    count_query = sa.select(sa.func.count()).select_from(query.subquery())

    # apply pagination to query
    if limit != -1:
        query = query.offset(offset).limit(limit)

    with Session() as session:
        count = session.scalar(count_query)
        if count is None:
            count = 0

        result = session.scalars(query).unique().all()
        items = [coerce_orm_to_strawberry(o, object_cls, nested_keys) for o in result]

        return PageInfo(
            offset=offset,
            limit=limit,
            count=len(items),
            total_count=count,
            items=items,
        )
