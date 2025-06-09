import asyncio
import datetime
import os
from typing import Callable

import aiofiles
import aiofiles.os as aos
import aiohttp
import requests
from humanize import naturalsize, precisedelta
from loguru import logger

from src.core.utils import get_semaphore_limit

from .index_file_parser import File, Filelist


def download_file_sync(file: File, to_folder: str) -> None:
    with requests.get(file.download_url) as resp:
        if resp.status_code != 200:
            logger.error(f"Failed to download {file.part!r}, got {resp.status_code!r}")
            return

        out_fpath = os.path.join(to_folder, file.filename)
        with open(out_fpath, "wb") as fp:
            fp.write(resp.content)


async def download_file_async(
    semaphore: asyncio.Semaphore, file: File, to_folder: str | Callable[[File], str]
) -> None:
    async with semaphore, aiohttp.ClientSession() as session:
        async with session.get(file.download_url) as resp:
            if resp.status != 200:
                logger.error(f"Failed to download {file.part!r}, got {resp.status!r}")
                return

            file_content = await resp.read()

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
                await fp.write(file_content)


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
