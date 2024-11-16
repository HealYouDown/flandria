import asyncio
import datetime
import io
import os
import zipfile
from typing import Callable

import aiofiles
import aiofiles.os as aos
import aiohttp
import requests
from humanize import naturalsize, precisedelta
from loguru import logger

from src.core.utils import get_semaphore_limit

from .index_file_parser import File, Filelist


def validate_zip(file: File, zipf: zipfile.ZipFile) -> bool:
    if not len(zipf.filelist) == 1:
        logger.error(f"Found more than one file in downloaded zip: {zipf.filelist!r}")
        return False

    zipf_file = zipf.filelist[0]
    if not zipf_file.filename == file.filename:
        logger.error(
            f"Expected {file.filename!r}, but zip contains {zipf_file.filename!r}"
        )
        return False

    if not zipf_file.file_size == file.size:
        logger.error(
            f"{zipf_file.filename} has a different size than according to "
            f"the index file: {zipf_file.file_size} (Zipfile) vs. "
            f"{file.size} (Version.bin) "
        )
        return False

    return True


def download_file_sync(file: File, to_folder: str) -> None:
    with requests.get(file.download_url) as resp:
        if resp.status_code != 200:
            logger.error(f"Failed to download {file.part!r}, got {resp.status_code!r}")
            return

    try:
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zipf:
            if not validate_zip(file, zipf):
                return

            out_fpath = os.path.join(to_folder, file.filename)
            with open(out_fpath, "wb") as fp:
                fp.write(zipf.read(zipf.filelist[0]))

    except zipfile.BadZipFile as e:
        logger.error(f"Bad ZipFile for for {file.part!r}: {e}")


async def download_file_async(
    semaphore: asyncio.Semaphore, file: File, to_folder: str | Callable[[File], str]
) -> None:
    async with semaphore, aiohttp.ClientSession() as session:
        async with session.get(file.download_url) as resp:
            if resp.status != 200:
                logger.error(f"Failed to download {file.part!r}, got {resp.status!r}")
                return

            try:
                zip_data = await resp.read()
            except Exception as e:
                logger.error(f"Failed to download {file.part!r}: {e!r}")
                return

    try:
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zipf:
            if not validate_zip(file, zipf):
                return

            # Check that to_folder exists, as it isn't checked beforehand
            # for async download, only sync.
            if isinstance(to_folder, str):
                folder = to_folder
            else:
                folder = to_folder(file)

            folder_exists = await aos.path.exists(folder)
            if not folder_exists:
                await aos.makedirs(folder, exist_ok=True)

            out_fpath = os.path.join(folder, file.filename)
            async with aiofiles.open(out_fpath, "wb") as fp:
                await fp.write(zipf.read(zipf.filelist[0]))

    except zipfile.BadZipFile as e:
        logger.error(f"Bad ZipFile for for {file.part!r}: {e}")


def download_files(
    filelist: Filelist,
    to_folder: str | Callable[[File], str],
    sync: bool = False,
) -> None:
    """Downloads a list of files.

    Args:
        filelist (Filelist): List of files to download.
        to_folder (str | Callable[[File], str]): Save folder for the files.
        Given a callable function, it should return the path based on the File object.
        If the folder does not exist, it will be created.
        sync (bool): Whether to download the files using sync insteaf of async.
    """
    total_filesize = sum(file.size for file in filelist)
    logger.info(
        f"Starting download of {len(filelist)} "
        f"files ({naturalsize(total_filesize)})"
    )

    start_dt = datetime.datetime.now(datetime.UTC)

    if sync:
        for file in filelist:
            if isinstance(to_folder, str):
                folder = to_folder
            else:
                folder = to_folder(file)

            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)

            download_file_sync(file, folder)
    else:
        semaphore_limit = get_semaphore_limit()
        logger.info(f"Starting {semaphore_limit} download tasks")

        semaphore = asyncio.Semaphore(semaphore_limit)

        # new_event_loop because calling the download function
        # twice if we were to use get_event_loop() would result in an error,
        # because we close it at the end.
        loop = asyncio.new_event_loop()

        tasks = [
            loop.create_task(download_file_async(semaphore, file, to_folder))
            for file in filelist
        ]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    end_dt = datetime.datetime.now(datetime.UTC)

    logger.success(f"Finished in {precisedelta(end_dt - start_dt)}")
