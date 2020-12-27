import os
import shutil
import typing

from flask import current_app
from PIL import Image
from webapp.extensions import db
from webapp.models import (ItemList, Monster, MonsterSkill, Npc, PetSkill,
                           PlayerSkill)

from database_updater.constants import (PALETTES_FOLDER, PUBLIC_ASSETS_FOLDER,
                                        TEMP_FOLDER)


def get_needed_icons(model) -> typing.List[str]:
    icons = set(
        [row[0] for row in db.session.query(model.icon).all()]
    )

    if model == ItemList:
        # Add gelt icon
        icons.add("def004.png")

    return icons


def get_icon_name(palette_name: str, num: int) -> str:
    if num < 10:
        return f"{palette_name}00{num}.png"

    elif num < 100:
        return f"{palette_name}0{num}.png"

    return f"{palette_name}{num}.png"


def cut_palette(palette_name_with_extension: str) -> None:
    fname, extension = palette_name_with_extension.split(".")

    if len(fname) > 5:  # no palette fname
        return

    if len(fname) == 5:
        palette_name = fname[0:3]
        size = int(fname[3:5])

    else:
        palette_name = fname
        size = 32

    palette_img = Image.open(os.path.join(PALETTES_FOLDER,
                                          palette_name_with_extension))

    x = 0
    y = 0
    x_max = 16 * size

    for i in range(16*16):
        icon_name = get_icon_name(palette_name, i)

        # Cutout icon
        icon = palette_img.crop((x, y, x+size, y+size))

        x += size
        if x == x_max:
            x = 0
            y += size

        icon.save(os.path.join(TEMP_FOLDER, icon_name))


def copy_needed_icons(model, folder_name: str, crop: bool = False) -> None:
    needed_icons = get_needed_icons(model)
    all_icons = [fname for fname in os.listdir(TEMP_FOLDER)
                 if fname.endswith(".png")]

    fpath = os.path.join(PUBLIC_ASSETS_FOLDER, folder_name)
    if not os.path.exists(fpath):
        os.makedirs(fpath)

    for icon in needed_icons:
        if icon not in all_icons:
            # icon is missing :(
            current_app.logger.warning(f"Missing {folder_name}: {icon}.")
            continue

        from_fpath = os.path.join(TEMP_FOLDER, icon)
        to_fpath = os.path.join(fpath, icon)

        if crop:
            Image.open(from_fpath).crop((0, 0, 50, 47)).save(to_fpath)
        else:
            shutil.copyfile(from_fpath, to_fpath)


def update_icons() -> None:
    # Cuts palettes and stores icons in TEMP Folder
    for palette_name in os.listdir(PALETTES_FOLDER):
        current_app.logger.info(f"Cutting Palette {palette_name}")
        cut_palette(palette_name)

    current_app.logger.info("Copying item icons")
    copy_needed_icons(ItemList, "item_icons")

    current_app.logger.info("Copying monster icons")
    copy_needed_icons(Monster, "monster_icons", True)

    current_app.logger.info("Copying npc icons")
    copy_needed_icons(Npc, "npc_icons", True)

    current_app.logger.info("Copying skill icons")
    copy_needed_icons(PlayerSkill, "skill_icons")

    current_app.logger.info("Copying monster skill icons")
    # Goes to same folder as normal skill icons
    copy_needed_icons(MonsterSkill, "skill_icons")

    current_app.logger.info("Copying pet skill icons")
    # Goes to same folder as normal skill icons
    copy_needed_icons(PetSkill, "skill_icons")
