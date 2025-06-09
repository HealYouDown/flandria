import json
import os
import re
from dataclasses import dataclass
from typing import Container

import requests
from loguru import logger

from src.core.constants import PATCHSERVER_URL, TMP_PATH


@dataclass
class File:
    part: str
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
        return f"{PATCHSERVER_URL}/{self.part}"


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
    metadata_fpath = os.path.join(TMP_PATH, "metadata.json")

    # Check if we have a cached metadata.json available for usage
    if not os.path.exists(metadata_fpath):
        logger.debug("Downloading metadata.json file because it does not exist.")
        download_url = f"{PATCHSERVER_URL}/metadata.json"
        with requests.get(download_url, stream=True) as resp:
            with open(metadata_fpath, "w") as fp:
                json.dump(resp.json(), fp)

    # Parse the index file and extract all information
    # uk1 and uk2 are probably related to how the launcher checks whether
    # a file needs to be updated, somehow related to timestamps, but no idea.
    with open(metadata_fpath, "r", encoding="utf-8") as fp:
        data = json.load(fp)

        files: list[File] = []
        for file_metadata in data:
            files.append(File(part=file_metadata["name"], size=file_metadata["size"]))
        return Filelist(files)
