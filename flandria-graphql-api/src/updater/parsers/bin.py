import enum
import struct
from dataclasses import dataclass
from typing import Any


class ColumnType(enum.Enum):
    integer = 0  # integer
    float = 1  # floating point number
    bool = 2  # bool, which is stored as 4 bytes
    string_12 = 3  # String with size 12
    string_32 = 4  # String with size 32
    string_128 = 5  # String with size 128

    @property
    def length(self) -> int:
        if self == ColumnType.string_12:
            return 12
        elif self == ColumnType.string_32:
            return 32
        elif self == ColumnType.string_128:
            return 128
        else:  # Int, Float, Boolean
            return 4


@dataclass
class Header:
    name: str
    c_type: ColumnType


def decode_string(bytes_: bytes) -> str:
    return bytes_.split(b"\x00")[0].decode("cp949")


def parse_bin(fpath: str) -> list[dict[str, int | float | bool | str | None]]:
    with open(fpath, "rb") as fp:
        row_count: int = struct.unpack("i", fp.read(4))[0]
        row_length: int = struct.unpack("i", fp.read(4))[0]  # noqa: F841
        column_count: int = struct.unpack("i", fp.read(4))[0]

        headers = [
            Header(
                name=decode_string(fp.read(32)).strip(),
                c_type=ColumnType(struct.unpack("i", fp.read(4))[0]),
            )
            for _ in range(column_count)
        ]

        rows: list[list[Any]] = []
        for _ in range(row_count):
            # An integer with the row id, 0, 1, 2, 3, 4, ...
            row_id = struct.unpack("<L", fp.read(4))[0]

            row = [row_id]
            for header in headers:
                value_as_bytes: bytes = fp.read(header.c_type.length)

                if header.c_type == ColumnType.integer:
                    value = struct.unpack("<l", value_as_bytes)[0]
                elif header.c_type == ColumnType.float:
                    value = round(struct.unpack("<f", value_as_bytes)[0], 6)
                elif header.c_type == ColumnType.bool:
                    value = bool(struct.unpack("<L", value_as_bytes)[0])
                elif header.c_type == ColumnType.string_12:
                    value = decode_string(value_as_bytes)
                elif header.c_type == ColumnType.string_32:
                    value = decode_string(value_as_bytes)
                elif header.c_type == ColumnType.string_128:
                    value = decode_string(value_as_bytes)
                else:
                    raise ValueError(f"Unknown column type: {header.c_type}")

                if value == "#":
                    value = None

                row.append(value)
            rows.append(row)

        # add row_id header for dict comprehension
        headers.insert(0, Header(name="row_id", c_type=ColumnType.integer))

        return [
            {header.name: value for header, value in zip(headers, row)} for row in rows
        ]
