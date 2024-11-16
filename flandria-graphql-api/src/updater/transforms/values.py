from typing import Any


def value_if_not_equal(
    value: Any,
    compare_value: Any,
    else_: Any = None,
) -> Any | None:
    return value if value != compare_value else else_
