from typing import TYPE_CHECKING, Any, Type, TypeVar

import sqlalchemy as sa
import strawberry

from src.database.engine import Session

from .helpers import coerce_orm_to_strawberry, parse_nested_keys_from_selections
from .sqla_helpers import apply_join_options

if TYPE_CHECKING:
    from src.database.types import ModelCls

T = TypeVar("T")


def resolve_single(
    *,
    info: strawberry.Info,
    model_cls: "ModelCls",
    object_cls: Type[T],
    pk: dict[str, Any],
) -> T | None:
    nested_keys = parse_nested_keys_from_selections(info.selected_fields)[
        info._raw_info.field_name
    ]

    pk_where_clause = sa.and_(*[getattr(model_cls, key) == v for key, v in pk.items()])
    query = sa.select(model_cls).where(pk_where_clause)
    if nested_keys:
        query = apply_join_options(query, model_cls, nested_keys)

    with Session() as session:
        res = session.scalars(query).first()
        if res is None:
            return None

        return coerce_orm_to_strawberry(res, object_cls, nested_keys)
