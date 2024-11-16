import enum


class Model3DClass(enum.Enum):
    SAINT = enum.auto()
    NOBLE = enum.auto()
    MERCENARY = enum.auto()
    EXPLORER = enum.auto()
    ALL = enum.auto()


class Model3DGender(enum.Enum):
    MALE = enum.auto()
    FEMALE = enum.auto()
    GENDERLESS = enum.auto()
