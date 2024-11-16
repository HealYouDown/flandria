import itertools
import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Iterable, Sequence

from src.core.case_insensitive_dict import CaseInsensitiveDict
from src.core.constants import UPDATER_DATA_PATH
from src.updater.parsers import parse_bin, parse_dat

if TYPE_CHECKING:
    from src.updater.schema import RequiredFiles


def load_file(filename: str) -> Sequence[dict[str, Any]]:
    path = os.path.join(UPDATER_DATA_PATH, filename)
    _, ext = os.path.splitext(filename)

    if ext == ".bin":
        return parse_bin(path)
    elif ext == ".dat":
        return parse_dat(path)
    else:
        raise ValueError(f"Encountered unknown extension {ext!r} for {path!r}")


T_BIN_TYPES = int | float | bool | str | None


@dataclass
class FileData:
    server_data: list[dict[str, T_BIN_TYPES]]
    client_data: list[dict[str, T_BIN_TYPES]]
    string_data: list[dict[str, str]]
    description_data: list[dict[str, str]]

    client_lookup: CaseInsensitiveDict[dict[str, T_BIN_TYPES]] = field(init=False)
    string_lookup: CaseInsensitiveDict[dict[str, str]] = field(init=False)
    description_lookup: CaseInsensitiveDict[dict[str, str]] = field(init=False)

    @staticmethod
    def _transform_to_o1(data: Iterable[dict], key: str) -> CaseInsensitiveDict:
        return CaseInsensitiveDict({row[key]: row for row in data})

    @classmethod
    def from_files(cls, files: "RequiredFiles"):
        server_data = list(
            itertools.chain.from_iterable(
                load_file(filename) for filename in files.server_files
            )
        )
        client_data = list(
            itertools.chain.from_iterable(
                load_file(filename) for filename in files.client_files
            )
        )
        string_data = list(
            itertools.chain.from_iterable(
                load_file(filename) for filename in files.string_files
            )
        )
        description_data = list(
            itertools.chain.from_iterable(
                load_file(filename) for filename in files.description_files
            )
        )

        return cls(
            server_data=server_data,
            client_data=client_data,
            string_data=string_data,
            description_data=description_data,
        )

    def __post_init__(self):
        # client, string and description data are transformed for O(1) lookup
        # as they only contain data related to a key in server_data.

        # client data acts as server data if no server data is given, so we don't need
        # to transform it. (it doesn't have a code key)
        if self.server_data:
            self.client_lookup = self._transform_to_o1(self.client_data, key="코드")

        self.string_lookup = self._transform_to_o1(self.string_data, key="Code")
        self.description_lookup = self._transform_to_o1(
            self.description_data, key="Code"
        )
