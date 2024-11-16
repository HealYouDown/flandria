import os
import re
import shutil
from dataclasses import dataclass
from typing import Container

import requests
from loguru import logger

from src.core.constants import PATCHSERVER_URL, TMP_PATH


@dataclass
class File:
    part: str
    unknown1: int
    unknown2: int
    size: int

    @property
    def path(self) -> str:
        """Returns the filepath part of the file.

        e.g. Bin/Setting/FaceTable.ini -> Bin/Setting

        Returns:
            str: Filepath
        """
        return self.part.rsplit("/", 1)[0]

    @property
    def filename(self) -> str:
        """Returns the filename part of the file.

        e.g. Bin/Setting/FaceTable.ini -> FaceTable.ini

        Returns:
            str: Filename
        """
        return self.part.rsplit("/", 1)[-1]

    @property
    def download_url(self) -> str:
        return f"{PATCHSERVER_URL}/{self.part}.zip"


class Filelist(list[File]):
    def find_by_filename(self, filename: str) -> "Filelist":
        """Returns all files matching the given filename.

        Usage:
        >>> filelist.find_by_filename("lm00202.nif")
        >>> Filelist(...)

        Args:
            filename (str): Filename to look for.

        Returns:
            list[File]: Matching file objects.
        """
        return Filelist([file for file in self if file.filename == filename])

    def find_by_filenames(self, filenames: Container[str]) -> "Filelist":
        """Returns all files matching any of the given filenames

        Usage:
        >>> filelist.find_by_filenames(["s_file1.bin", "s_file2.bin"])
        >>> Filelist(...)

        Args:
            filenames (Sequence[str]): Filenames to look for.

        Returns:
            list[File]: Matching file objects.
        """
        return Filelist([file for file in self if file.filename in filenames])

    def find_by_filepath(self, filepath: str) -> "Filelist":
        """Returns all files matching the given path from the start.

        Usage:
        >>> filelist.find_by_filepath("Data/Actor/Pet")
        >>> Filelist(...)

        Args:
            filepath (str): Filepath to look for.

        Returns:
            list[File]: Matching file objects.
        """
        return Filelist([file for file in self if file.path.startswith(filepath)])

    def find_by_regex(self, pattern: re.Pattern) -> "Filelist":
        """Returns all files where the any part of the path matches the given regular expression.

        Usage:
        >>> pattern = re.compile("\\.nif$")
        >>> filelist.find_by_regex(pattern)
        >>> Filelist(...)

        Args:
            pattern (re.Pattern): Regular expression pattern.

        Returns:
            list[File]: Matching file objects.
        """
        return Filelist(file for file in self if pattern.search(file.part) is not None)


def get_filelist_from_index() -> Filelist:
    """Parses the version.bin file. The version.bin file is an index about
    all available files from the patch server for florensia.

    If the file is not locally available (in the tmp folder), the fill will be
    downloaded before proceeding and stored to tmp.

    Returns:
        Filelist: A list of all File objects which contain
        data about the available files in the index.
    """

    index_fpath = os.path.join(TMP_PATH, "version.bin")

    # Check if we have a cached version.bin available for usage
    if not os.path.exists(index_fpath):
        logger.debug("Downloading version.bin file because it does not exist.")
        download_url = f"{PATCHSERVER_URL}/version.bin"
        with requests.get(download_url, stream=True) as resp:
            with open(index_fpath, "wb") as fp:
                shutil.copyfileobj(resp.raw, fp)

    # Parse the index file and extract all information
    # uk1 and uk2 are probably related to how the launcher checks whether
    # a file needs to be updated, somehow related to timestamps, but no idea.
    with open(index_fpath, "r", encoding="euc_kr") as fp:
        lines = fp.read().splitlines(keepends=False)[1:]
        files = []
        for line in lines:
            part, rest = line.split("| ")
            uk1, uk2, size = tuple(int(i) for i in rest.split(" "))
            files.append(File(part.strip(), uk1, uk2, size))
        return Filelist(files)
