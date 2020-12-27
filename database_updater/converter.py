import re
import struct
from typing import Dict, List

# Thanks to Noxx for the inital implementation in FloBase on which I could
# build on.
# Helped a lot to not have to figure all of this stuff out.. :)


def columntypes(t: int) -> int:
    if t in [0, 1, 2]:
        return 4
    elif t == 3:
        return 12
    elif t == 4:
        return 32
    elif t == 5:
        return 128
    else:
        return 0


def bin2list(filepath: str) -> List[Dict]:
    """Converts a given florensia .bin file to a
    list containting column headers as keys, row data
    as values.

    Args:
        filepath (str): Filepath to the .bin file.

    Returns:
        List[Dict]: List with all row items.
    """

    # 4 bytes: number_of_rows
    # 4 bytes: dataset_length
    # 4 bytes: number_of_columns
    # number_of_columns *
    #     32 bytes: column_name
    #     4 bytes: column_length
    # number_of_rows *
    #     4 bytes: trash
    #     column_length bytes: data
    # 4 bytes: trash

    # Decodes file
    with open(filepath, "rb") as fp:
        number_of_rows = struct.unpack("i", fp.read(4))[0]
        dataset_length = struct.unpack("i", fp.read(4))[0]  # noqa F841
        number_of_columns = struct.unpack("i", fp.read(4))[0]

        column_headers = []
        for _ in range(number_of_columns):
            byte_seq = fp.read(32)

            # Workaround for some malformed byte sequence, probably corrupt
            # files by AHA...
            if byte_seq == (b"\xba\xb8\xbb\xf3\xbc"
                            b"\xf6\xb7\xae55\x00\x00"
                            b"\x01\x00\x00\x00(B\n\x08"
                            b"\x0f\x1b\x00\x80 \xff\xa9"
                            b"\x0b\xc8\xff\xa9\x0b"):
                cname = "보상수량55"
            elif byte_seq == (b"\xba\xb8\xbb\xf3\xbc\xf6\xb7"
                              b"\xae22\x00\x00\x01\x00\x00\x00"
                              b"\xaa\x10q\xed\x00z\x00\x80\xc8"
                              b"\t\xd7\x06\xe0\n\xd7\x06"):
                cname = "보상수량22"
            else:
                cname = re.sub(b"\x00.*", b"", byte_seq).decode("euc_kr")

            length = columntypes(struct.unpack("i", fp.read(4))[0])
            column_headers.append({
                "name": cname.strip(),
                "length": length
            })

        rows = []
        for _ in range(number_of_rows):
            _ = fp.read(4)  # trash
            row = {}

            for header in column_headers:
                byte_data = fp.read(header["length"])

                if header["length"] != 4:  # string
                    try:
                        byte_seq = re.sub(b"\x00.*", b"", byte_data)
                        data = byte_seq.decode("euc_kr").strip()
                    except UnicodeDecodeError:
                        try:
                            # Workaround for some bad strings in dress file
                            byte_seq = re.sub(b"\x00.*",
                                              b"",
                                              byte_data[2:(len(byte_data)-1)])
                            data = byte_seq.decode("euc_kr").strip()
                        except UnicodeDecodeError:
                            # if this also fails, AHA messed up (happens a lot)
                            # so we just take the string and keep the errors
                            byte_seq = re.sub(b"\x00.*", b"", byte_data)
                            data = byte_seq.decode(
                                "euc_kr", errors="ignore").strip()

                else:  # number
                    data = struct.unpack("L", byte_data)[0]

                row[header["name"]] = data

            rows.append(row)

    return rows


def dat2list(filename: str) -> List[Dict]:
    """Converts a given florensia .dat file to
    a list containing column headers as keys, row
    data as values.

    Args:
        filename (str): Filepath to the .dat file.

    Returns:
        List[Dict]: List with all row items.
    """

    with open(filename, "r", encoding="utf-16") as fp:
        lines = fp.readlines()

    # First line of .dat files contain only the headers separated
    # by tabs.
    headers = [line.strip() for line in lines[0].split("\t")]

    # Everything except the headers and the __END at the bottom are
    # data rows
    lines = lines[1:len(lines)-1]

    # Splits rows into one big list where each child-list is a single row with
    # single values
    rows = [[val.strip() for val in line.split("\t")]
            for line in lines]

    # All rows have \n at the end which is included in the list as ''.
    # Therefore, we only loop through all items in the list except
    # the last one.

    return [
        {
            headers[index]: value
            for index, value in enumerate(row[:-1])
        } for row in rows
    ]
