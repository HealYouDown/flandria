import os
import re
from typing import Iterable

import sqlalchemy as sa
import sqlalchemy.orm as orm
from PIL import Image

from src.core.constants import (
    FALLBACK_ACTOR_ICON,
    FALLBACK_ITEM_ICON,
    FALLBACK_SKILL_ICON,
)
from src.database.engine import engine
from src.database.models import (
    ItemList,
    Monster,
    MonsterSkill,
    Npc,
    PetSkill,
    PlayerSkill,
)

ICONS_PER_ROW = 16
ICONS_PER_COLUMN = 16


def get_icons_from_palette(fpath: str) -> dict[str, Image.Image]:
    palette_name, _ = os.path.splitext(os.path.basename(fpath))
    palette = Image.open(fpath)

    # check if the palette name has a size "parameter"
    size = 32
    if (match := re.match(r"^\w{3}(\d+)$", palette_name)) is not None:
        size = int(match.group(1))

    count = 0
    icons = {}
    for y in range(0, ICONS_PER_COLUMN * size, size):
        for x in range(0, ICONS_PER_ROW * size, size):
            icon_name = f"{palette_name}_{count:0>3}.png"
            icon = palette.crop((x, y, x + size, y + size))
            icons[icon_name] = icon

            count += 1

    return icons


def crop_actor_icon(fpath: str) -> Image.Image:
    # Actor icons have a lot of transparent pixel data
    # on the bottom right, which we cut
    return Image.open(fpath).crop((0, 0, 50, 47))


def get_actor_icons() -> set[str]:
    with orm.Session(engine) as session:
        query = sa.union(
            sa.select(Monster.icon),
            sa.select(Npc.icon),
        )
        actor_icons = session.scalars(query).all()
        return set(actor_icons) | {FALLBACK_ACTOR_ICON}


def get_item_icons() -> set[str]:
    with orm.Session(engine) as session:
        query = sa.select(ItemList.icon)
        item_icons = session.scalars(query).all()
        return set(item_icons) | {FALLBACK_ITEM_ICON}


def get_skill_icons() -> set[str]:
    with orm.Session(engine) as session:
        query = sa.union(
            sa.select(MonsterSkill.icon),
            sa.select(PlayerSkill.icon),
            sa.select(PetSkill.icon),
        )
        skill_icons = session.scalars(query).all()
        return set(skill_icons) | {FALLBACK_SKILL_ICON}


def get_palette_filenames_from_icons(icons: Iterable[str]) -> set[str]:
    """Returns all required palette names from the given icon names.

    Args:
        icons (Iterable[str]): List of icon names to iterate.

    Returns:
        set[str]: Set of unique palette names for the given icon list.
    """
    return set(f"{icon.split('_')[0]}.png" for icon in icons)
