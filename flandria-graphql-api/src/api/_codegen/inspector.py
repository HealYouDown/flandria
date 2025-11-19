import enum
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, cast

import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.column_types import RGB

if TYPE_CHECKING:
    from src.database.types import ModelCls

# List of columns that should be annotated with strawberry.Private to not expose them
PRIVATE_COLUMNS = []


@dataclass(frozen=True)
class InspectedORMField:
    name: str
    type_: type
    is_nullable: bool
    is_list: bool = field(default=False)
    is_private: bool = field(default=False)

    forced_annotation: str | None = field(default=None)
    exclude_from_filters: bool = field(default=False)

    @property
    def is_enum(self) -> bool:
        return issubclass(self.type_, enum.Enum)

    @property
    def annotation_requires_forwardref(self) -> bool:
        # basic types and enums don't require a forward ref
        is_basic_type = any(self.type_ is (j) for j in (int, bool, float, str))
        return not (is_basic_type or self.is_enum)

    @property
    def strawberry_annotation(self) -> str:
        if self.forced_annotation is not None:
            return self.forced_annotation

        if self.annotation_requires_forwardref:
            annotation = f'"{self.type_.__name__}"'
        else:
            annotation = self.type_.__name__
            if self.is_enum:
                # requires enums to always be imported as from src.api import enums
                annotation = f"enums.{annotation}"

        if self.is_list:
            annotation = f"list[{annotation}]"
        elif self.is_nullable:
            annotation = f"Optional[{annotation}]"

        if self.is_private:
            annotation = f"strawberry.Private[{annotation}]"

        return annotation


def get_relationship_is_optional(relationship: orm.RelationshipProperty) -> bool:
    # taken from
    # https://github.com/strawberry-graphql/strawberry-sqlalchemy/blob/f9c09a156f91abce4ca814b743f1ea6421ecdeb3/src/strawberry_sqlalchemy_mapper/mapper.py#L397
    if relationship.direction in [orm.ONETOMANY, orm.MANYTOMANY]:
        # many on other side means it's optional always
        return True
    else:
        assert relationship.direction == orm.MANYTOONE
        # this model is the one with the FK
        for local_col, _ in relationship.local_remote_pairs or []:
            if local_col.nullable:
                return True
        return False


def inspect_model(model_cls: "ModelCls") -> list[InspectedORMField]:
    fields: list[InspectedORMField] = []
    inspector = sa.inspect(model_cls)

    for column_name, column in inspector.columns.items():
        # Hacky support for our custom types
        if column.type.__class__ is RGB:
            fields.append(
                InspectedORMField(
                    name=column_name,
                    type_=int,
                    forced_annotation="Optional[list[int]]",
                    is_nullable=True,
                    exclude_from_filters=True,
                )
            )
            continue

        fields.append(
            InspectedORMField(
                name=column_name,
                type_=column.type.python_type,
                is_nullable=cast(bool, column.nullable),
                is_private=column in PRIVATE_COLUMNS,
            )
        )

    for rel_name, rel_property in inspector.relationships.items():
        fields.append(
            InspectedORMField(
                name=rel_name,
                type_=rel_property.entity.class_,
                is_list=cast(bool, rel_property.uselist),
                is_nullable=get_relationship_is_optional(rel_property),
            )
        )

    return fields
