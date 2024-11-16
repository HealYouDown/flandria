import re
from typing import TYPE_CHECKING, Any, ClassVar, Optional

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.exc import InvalidRequestError

if TYPE_CHECKING:
    from src.updater.schema import LoaderInfo


class Base(orm.DeclarativeBase):
    loader_info: ClassVar[Optional["LoaderInfo"]] = None

    @orm.declared_attr.directive
    def __tablename__(cls) -> str:
        # Converts CamelCase to snake_case with workarounds
        # to avoid HTTPMethod -> http_method instead of h_t_t_p_method
        name = cls.__name__
        pattern = r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])"
        tablename = re.sub(pattern, "_", name).lower()
        return tablename

    def as_dict(
        self,
    ) -> dict[str, Any]:
        result = {}
        inspector = sa.inspect(self.__class__)

        for column_name in inspector.columns.keys():
            result[column_name] = getattr(self, column_name)

        for relationship_name in inspector.relationships.keys():
            relationship = inspector.relationships[relationship_name]

            try:
                value = getattr(self, relationship_name)
                if relationship.uselist:
                    result[relationship_name] = [obj.as_dict() for obj in value]
                else:
                    result[relationship_name] = (
                        value.as_dict() if value is not None else None
                    )
            except InvalidRequestError:  # xxx is not available due to lazy='raise'
                if relationship.uselist:
                    result[relationship_name] = []
                else:
                    result[relationship_name] = None

        return result
