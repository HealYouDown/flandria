from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .base import Base

Model = Base
ModelCls = Type["Base"]
