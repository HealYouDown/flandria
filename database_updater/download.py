import io
import os
import typing
import zipfile
from multiprocessing import Pool

import requests
import tqdm
from flask import current_app

from database_updater.constants import (PALETTES_FOLDER, QUESTS_FOLDER,
                                        TEMP_FOLDER)
from database_updater.helpers import get_patchserver_file_urls


def download_file(url: str) -> typing.Union[None, str]:
    """Downloads given url to TEMP_FOLDER.

    Args:
        url (str): URL to download.

    Returns:
        Union[None, str]: If something went wrong, url is returned.
    """
    # Gets the filename from the url. Example url:
    # http://patch.florensia-online.eu/LIVE/Patch/Update/Data/Actor/Monster/lm00201/lm00201.png.zip
    fpath, fname = url.rsplit("/", maxsplit=1)
    fname = fname.replace(".zip", "")

    # Quests are stored to an extra 'quests' folder
    if "QuestData" in fpath:
        save_path = os.path.join(QUESTS_FOLDER, fname.lower())
    elif "Data/UI/Icon" in fpath:
        save_path = os.path.join(PALETTES_FOLDER, fname)
    else:
        save_path = os.path.join(TEMP_FOLDER, fname)

    # Request file from given url
    with requests.get(url) as req:
        # if file has any problems, the url is returned and
        # later logged to the user.
        if req.status_code != 200:
            return url

        try:
            # Unpack zip file and save file with content to the temp folder
            with zipfile.ZipFile(io.BytesIO(req.content)) as zipf:
                with open(save_path, "wb") as fp:
                    fp.write(zipf.read(fname))
        except zipfile.BadZipFile:
            # Zip file is corrupt and cannot be unpacked, url is
            # returned and later logged.
            return url


def download() -> None:
    """Function run from the CLI to initalize the download process."""
    # Get urls to download
    current_app.logger.info("Getting urls to download.")
    urls = get_patchserver_file_urls()
    current_app.logger.info(f"Found {len(urls)} urls.")

    # Create a pool for multiple downloads at the same time
    pool = Pool(processes=8)  # FIXME: CLI argument instead of hardcoding it

    # Start loop with tqdm, which prints a good looking statusbar of the
    # process.
    failed_files = []
    for status in tqdm.tqdm(pool.imap(download_file, urls),
                            total=len(urls),
                            desc="Download Status",
                            unit="Files"):
        if status:
            # Something went wrong and a string with the url was returned.
            failed_files.append(status)

    # Log failed files.
    for failed_file in failed_files:
        current_app.logger.error(
            f"Failed to download or unpack {failed_file}.")
