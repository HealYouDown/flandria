import os
import re
import shutil
from typing import TYPE_CHECKING

from loguru import logger

from src.core.constants import MODELS_DATA_PATH
from src.core.downloader import Filelist, download_files, get_filelist_from_index

if TYPE_CHECKING:
    from src.core.downloader import File


def download_monster_models(skip_existing: bool):
    index_filelist = get_filelist_from_index()
    monster_pattern = re.compile(r"^Data/Actor/Monster/.*/.*(\.nif|\.kf|\.kfm)$")

    to_download = index_filelist.find_by_regex(monster_pattern)
    to_download += index_filelist.find_by_filepath(r"Data/Actor/Monster/Textures_low")

    def _to_folder(file: "File") -> str:
        return os.path.join(MODELS_DATA_PATH, "monster", file.path.split("/")[-1])

    if skip_existing:
        to_download = Filelist(
            [
                file
                for file in to_download
                if not os.path.exists(os.path.join(_to_folder(file), file.filename))
            ]
        )
        if not to_download:
            logger.info("Skipping download of monster models, all already present")
            return

    download_files(
        to_download,
        to_folder=_to_folder,
    )


def download_npc_models(skip_existing: bool):
    index_filelist = get_filelist_from_index()
    npc_pattern = re.compile(r"^Data/Actor/NPC/.*/.*/.*(\.nif|\.kf|\.kfm)$")
    to_download = index_filelist.find_by_regex(npc_pattern)
    to_download += index_filelist.find_by_filepath(r"Data/Actor/NPC/Textures_low")

    def _to_folder(file: "File") -> str:
        return os.path.join(MODELS_DATA_PATH, "npc", file.path.split("/")[-1])

    if skip_existing:
        to_download = Filelist(
            [
                file
                for file in to_download
                if not os.path.exists(os.path.join(_to_folder(file), file.filename))
            ]
        )
        if not to_download:
            logger.info("Skipping download of npc models, all already present")
            return

    download_files(
        to_download,
        to_folder=_to_folder,
    )


def download_item_models(skip_existing: bool):
    index_filelist = get_filelist_from_index()

    prefix = r"^Data/Actor/User/Item"
    item_pattern = re.compile(
        prefix + r"/item_(hef|hem|hnf|hnm|hsf|hsm|hwf|hwm|not)/\w+\.nif$"
    )
    texture_pattern = re.compile(
        prefix
        + r"item_(hef|hem|hnf|hnm|hsf|hsm|hwf|hwm|not)/Textures_low/\w+\.(tga|png|dds)$"
    )

    to_download = index_filelist.find_by_regex(item_pattern)
    to_download += index_filelist.find_by_regex(texture_pattern)

    def _to_folder(file: "File") -> str:
        parts = file.path.split("/")
        if parts[-1] == "Textures_low":
            # items/hef/Textures_low/<file>
            return os.path.join(MODELS_DATA_PATH, "items", parts[-2], "Textures_low")
        else:
            # items/hef/<file>.nif
            return os.path.join(MODELS_DATA_PATH, "items", parts[-1])

    if skip_existing:
        to_download = Filelist(
            [
                file
                for file in to_download
                if not os.path.exists(os.path.join(_to_folder(file), file.filename))
            ]
        )
        if not to_download:
            logger.info("Skipping download of item models, all already present")
            return

    download_files(
        to_download,
        to_folder=_to_folder,
    )


def download_model_files(skip_existing: bool) -> None:
    if not skip_existing:
        if os.path.exists(MODELS_DATA_PATH):
            shutil.rmtree(MODELS_DATA_PATH)

    logger.info("Downloading monster models")
    download_monster_models(skip_existing)

    logger.info("Downloading npc models")
    download_npc_models(skip_existing)

    logger.info("Downloading item models")
    download_item_models(skip_existing)
