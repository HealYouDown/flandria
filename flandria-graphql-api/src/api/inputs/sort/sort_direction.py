import enum

import strawberry


@strawberry.enum
class SortDirection(enum.Enum):
    ASC = enum.auto()
    DESC = enum.auto()
