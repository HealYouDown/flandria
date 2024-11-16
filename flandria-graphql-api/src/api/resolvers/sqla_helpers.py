from dataclasses import asdict
from typing import TYPE_CHECKING, Any, Callable, TypeVar, cast

import sqlalchemy as sa
import sqlalchemy.orm as orm
import strawberry
from strawberry.types.unset import UnsetType

from src.api.inputs import SortDirection
from src.api.inputs.filters.scalar_filters import ScalarFilter
from src.core.enums import EffectCode
from src.database.models import Effect

if TYPE_CHECKING:
    from sqlalchemy.orm.strategy_options import _AbstractLoad

    from src.database.types import ModelCls

    from .helpers import NestedDict
    from .pagination_resolver import Filter, OrderBy

T = TypeVar("T")


def apply_join_options(
    query: sa.Select[tuple[T]],
    model_cls: "ModelCls",
    nested_keys: "NestedDict",
) -> sa.Select[tuple[T]]:
    options = []

    def r(
        m: "ModelCls",
        nk: "NestedDict",
        parent_opt: "_AbstractLoad | None",
    ) -> None:
        insp = sa.inspect(m)
        for key, next_keys in nk.items():
            relationship = insp.relationships[key]
            declared_relatiopnship = getattr(m, key)
            # TODO: Depending on the relationship, we should probably decide between joinedload and selectinload
            if parent_opt:
                opt = parent_opt.selectinload(declared_relatiopnship)
            else:
                opt = orm.selectinload(declared_relatiopnship)

            if next_keys:
                target_cls = relationship.entity.class_
                r(target_cls, next_keys, opt)
            else:  # leaf ends here
                options.append(opt)

    r(model_cls, nested_keys, None)
    return query.options(*options)


def apply_filters(
    query: sa.Select[tuple[T]],
    model_cls: "ModelCls",
    filter: "Filter",
) -> sa.Select[tuple[T]]:
    FILTER_FUNCTIONS: dict[
        str, Callable[[orm.InstrumentedAttribute, Any], sa.ClauseElement]
    ] = {
        "eq": lambda col, val: col == val,
        "ne": lambda col, val: col != val,
        "in_": lambda col, val: col.in_(val),
        "like": lambda col, val: col.like(val),
        "ilike": lambda col, val: col.ilike(val),
        "gt": lambda col, val: col > val,
        "ge": lambda col, val: col >= val,
        "lt": lambda col, val: col < val,
        "le": lambda col, val: col <= val,
        "between": lambda col, val: col.between(*val),
    }

    def r(
        q: sa.Select[tuple[T]],
        m: "ModelCls",
        f: "Filter",
        parent_m: "ModelCls | None" = None,
    ) -> tuple[sa.Select[tuple[T]], list[sa.ColumnClause]]:
        clauses = []
        insp = sa.inspect(m)

        for key in f.__dataclass_fields__.keys():
            # value is either UNSET or {[key]: <value>}
            # value is either a scalar or another filter (relationships)
            value: "Filter | UnsetType" = getattr(f, key)
            if value is strawberry.UNSET:
                continue
            assert not isinstance(value, UnsetType)  # type guard

            # due to "one_of=True" for our scalar filters, there will be only one filter_key
            try:
                filter_key, value_to_filter = next(
                    (k, v)
                    for k, v in asdict(value).items()
                    if v is not strawberry.UNSET
                )
            except StopIteration:  # one_of limits the result to at most 1 key, but 0 passes validation as well
                continue

            if isinstance(value, ScalarFilter):
                # FIXME:
                # Workaround to support 1:n filter for effects
                # Not noice, but it's the only 1:n filter we technically need right now
                if key == "effect_code" and m is Effect and filter_key == "in_":
                    assert hasattr(parent_m, "effects")
                    assert hasattr(parent_m, "code")

                    effects = cast(list[EffectCode], value_to_filter)

                    code_column = cast(orm.InstrumentedAttribute[str], parent_m.code)  # type: ignore
                    effects_declaration = cast(
                        orm.InstrumentedAttribute[list[Effect]], parent_m.effects
                    )

                    # We use a subquery so that our count query still returns the correct result
                    subquery = (
                        sa.select(
                            code_column.label("code"),
                            sa.func.count(Effect.effect_code).label(
                                "count_matching_effects"
                            ),
                        )
                        .join(Effect, effects_declaration)
                        .where(Effect.effect_code.in_(effects))
                        .group_by(code_column)
                        .subquery()
                    )
                    q = q.join(
                        subquery,
                        onclause=code_column == subquery.c.code,
                    ).where(subquery.c.count_matching_effects >= len(effects))

                else:
                    column: orm.InstrumentedAttribute[Any] = getattr(m, key)
                    filter_func = FILTER_FUNCTIONS[filter_key]
                    clauses.append(filter_func(column, value_to_filter))
            else:  # if it's not a scalar filter, it's a filter on a relationship
                if key not in insp.relationships:
                    raise KeyError(
                        f"Can't filter for unknown non-scalar member {key!r} of {model_cls!r}"
                    )

                rel_property = insp.relationships[key]
                rel_declaration = getattr(m, key)
                target_cls: "ModelCls" = rel_property.entity.class_

                # we join by our defined relationship attribute on the model instead of joining the target_cls
                # so that primaryjoin on-clauses are respected. Otherwise sqlalchemy has no idea how to join certain
                # classes like monster -> messages, as the relationship is dynamically defined on the parent mixin.

                # For our effect filter above to work, we're not allowed to join the tables
                if target_cls is not Effect:
                    q = q.join(rel_declaration, isouter=False)

                q, c = r(q, target_cls, value, parent_m=m)
                clauses.extend(c)

        return q, clauses

    query, clauses = r(query, model_cls, filter)
    query = query.where(*clauses)

    return query


def apply_order_by(
    query: sa.Select[tuple[T]],
    model_cls: "ModelCls",
    order_by: list["OrderBy"],
) -> sa.Select[tuple[T]]:
    order_by_stmts = []
    for sort in order_by:
        value: "SortDirection"
        for column_name, value in asdict(sort).items():
            if value is strawberry.UNSET:
                continue

            if value == SortDirection.ASC:
                order_by_stmts.append(getattr(model_cls, column_name).asc())
            else:
                order_by_stmts.append(getattr(model_cls, column_name).desc())

    return query.order_by(*order_by_stmts)
