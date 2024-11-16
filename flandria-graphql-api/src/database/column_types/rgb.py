import sqlalchemy.types as types
from sqlalchemy import Dialect


def rgb_to_int(value: tuple[int, int, int]) -> int:
    r, g, b = value
    as_int = (r << 16) + (g << 8) + b
    return as_int


def int_to_rgb(value: int) -> tuple[int, int, int]:
    r = (value >> 16) & 0xFF
    g = (value >> 8) & 0xFF
    b = value & 0xFF
    return (r, g, b)


class RGB(types.TypeDecorator):
    impl = types.Integer
    cache_ok = True

    @property
    def python_type(self):
        return int

    def process_bind_param(
        self,
        value: tuple[int, int, int] | None,
        dialect: Dialect,
    ) -> int | None:
        if value is None:
            return None
        return rgb_to_int(value)

    def process_result_value(
        self,
        value: int | None,
        dialect: Dialect,
    ) -> tuple[int, int, int] | None:
        if value is None:
            return None
        return int_to_rgb(value)
