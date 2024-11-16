import os
import shutil

from loguru import logger

from src.assets.icons.helpers import (
    crop_actor_icon,
    get_actor_icons,
    get_icons_from_palette,
    get_item_icons,
    get_palette_filenames_from_icons,
    get_skill_icons,
)
from src.core.constants import ICONS_DATA_PATH
from src.core.downloader import download_files, get_filelist_from_index


def extract_icons(to_path: str) -> None:
    actor_icons = get_actor_icons()
    item_icons = get_item_icons()
    skill_icons = get_skill_icons()

    item_palettes = get_palette_filenames_from_icons(item_icons)
    skill_palettes = get_palette_filenames_from_icons(skill_icons)

    palette_icon_names = item_icons | skill_icons
    palette_names = item_palettes | skill_palettes

    for icon_name in actor_icons:
        icon_fpath = os.path.join(ICONS_DATA_PATH, icon_name)
        if not os.path.exists(icon_fpath):
            logger.warning(f"Missing actor icon {icon_name!r}")
            continue

        icon = crop_actor_icon(icon_fpath)

        out_fpath = os.path.join(to_path, icon_name)
        icon.save(out_fpath)

    for palette_name in palette_names:
        palette_fpath = os.path.join(ICONS_DATA_PATH, palette_name)
        if not os.path.exists(palette_fpath):
            logger.warning(f"Missing palette {palette_name!r}")
            continue

        palette_icons = get_icons_from_palette(palette_fpath)
        for icon_name, icon in palette_icons.items():
            # only save the icons that are required
            if icon_name in palette_icon_names:
                out_fpath = os.path.join(to_path, icon_name)
                icon.save(out_fpath)


def download_icon_files(skip_existing: bool) -> None:
    filelist = get_filelist_from_index()

    # actor icons
    required_filenames = [
        f.filename for f in filelist.find_by_filenames(get_actor_icons())
    ]
    # palettes for skills / items
    required_filenames += [
        f.filename
        for f in filelist.find_by_filenames(
            get_palette_filenames_from_icons(get_item_icons() | get_skill_icons())
        )
    ]

    if skip_existing:
        existing_files = os.listdir(ICONS_DATA_PATH)
        required_filenames = [
            filename
            for filename in required_filenames
            if filename not in existing_files
        ]

        if not required_filenames:
            logger.info(
                "Skipping download, as all files are already present. "
                "If you want to re-download everything, omit the "
                "--skip-existing flag."
            )
            return

    else:
        # Clear all files and re-download everything
        if os.path.exists(ICONS_DATA_PATH):
            shutil.rmtree(ICONS_DATA_PATH)

    if not os.path.exists(ICONS_DATA_PATH):
        os.makedirs(ICONS_DATA_PATH)

    files_to_download = filelist.find_by_filenames(required_filenames)
    download_files(files_to_download, ICONS_DATA_PATH)
