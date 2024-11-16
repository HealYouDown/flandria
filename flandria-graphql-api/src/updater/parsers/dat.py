from typing import Optional, Sequence


def parse_dat(
    fpath: str, headers: Optional[Sequence[str]] = None
) -> Sequence[dict[str, str]]:
    with open(fpath, "r", encoding="utf-16") as fp:
        lines = [line.strip() for line in fp.readlines()]

        if headers is None:
            headers = [line.strip() for line in lines[0].split("\t")]
            data_lines = lines[1:-1]
        else:
            data_lines = lines[:-1]
            assert len(headers) == len(data_lines[0].split("\t"))

        rows = [
            [val.strip() for val in line.strip().split("\t")] for line in data_lines
        ]

        return [{header: value for header, value in zip(headers, row)} for row in rows]
