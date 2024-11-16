import os
import re
import struct
from dataclasses import dataclass
from io import BufferedReader
from typing import Self

# tried writing a small parser like # See https://github.com/niftools/niflib/blob/e29166183e23c3477fb7e08d4523dd111440947e/src/kfm.cpp#L76
# but in the end, we only care about the filenames, so fuck that


def read_pascal_string(fp: BufferedReader):
    length = struct.unpack("I", fp.read(4))[0]
    s = fp.read(length)
    return s


def read_uint(fp: BufferedReader):
    return struct.unpack("I", fp.read(4))[0]


@dataclass
class KFMFile:
    nif_filename: str
    animations: list[str]

    @classmethod
    def read(cls, fpath: str) -> Self:
        with open(fpath, "rb") as fp:
            header = fp.readline()  # noqa: F841
            fp.read(1)
            nif_filename = os.path.basename(read_pascal_string(fp)).decode("ascii")
            master = read_pascal_string(fp)  # noqa: F841
            fp.read(16)
            num_actions = read_uint(fp)
            fp.read(4)

            # Extract all strings that end in .kf
            # ASCII printable characters from space (32) to tilde (126)
            pattern = re.compile(b"[ -~]{2,}\\.kf")
            all_strings: list[bytes] = pattern.findall(fp.read())

            # os.path.basename removes the .\\<filename> part
            actions = [os.path.basename(s.decode("ascii")) for s in all_strings]

            if len(actions) != num_actions:
                raise ValueError(
                    f"Expected {num_actions} in KFM file, found {len(actions)}"
                )

        return cls(nif_filename=nif_filename, animations=actions)
