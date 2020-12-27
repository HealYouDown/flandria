import typing
from database_updater.conversions import convert_integer

MAX_INT = 4294967295


def bonus_value_transform(
    value: int
) -> typing.Union[None, int, float]:
    return convert_integer(value) if value != 0 else None


def florensia_meter_transform(value: int) -> float:
    """Converts given value to florensia meters.

    Args:
        value (int): the given integer (e.g. 4700)

    Returns:
        float: The distance in meters (4700 = 47m)
    """
    return value / 100


def florensia_sea_meter_transform(value: int) -> float:
    """Converts given value to florensia meters for sea.

    Args:
        value (int): the given integer (e.g. 4700)

    Returns:
        float: The distance in meters (4700 = 470m)
    """
    return value / 10


def florensia_probability_transform(
    value: int,
    max_probability: int = 10000
) -> float:
    """Converts a given florensia probability to
    a float.

    Args:
        value (int): An integer between 0-10.000

    Returns:
        float: the normal probability value 10.0 = 10.0%. Rounded to 2
            decimal points.
    """
    # Max probability in florensia is often times 10.000
    return round((value / max_probability) * 100, 2)


def florensia_time_transform(value: int) -> float:
    return value / 1000
