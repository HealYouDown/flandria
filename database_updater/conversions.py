import struct
import typing


def convert_integer(value: int) -> typing.Union[int, float]:
    """Converts a given unsigned long integer to float.
    If the given long integer exceeds an unsigned integer,
    the value is not changed and a normal integer is returned.

    Args:
        value (int): A unsigned long integer.

    Returns:
        float: Float or default integer right back.
    """
    if 0 >= value <= 4294967295:
        return value

    # More information on:
    # https://docs.microsoft.com/de-de/cpp/c-language/conversions-from-unsigned-integral-types?view=msvc-160
    # https://stackoverflow.com/questions/24356579/why-is-1-0f-in-c-code-represented-as-1065353216-in-the-generated-assembly
    s = struct.pack("I", value)
    return round(struct.unpack("f", s)[0], 5)
