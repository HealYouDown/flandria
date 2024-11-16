import datetime
import itertools
import os
import re
import shutil
from typing import Any, Optional, Type, cast

import sqlalchemy as sa
from humanize import precisedelta
from loguru import logger

from src.core.constants import UPDATER_DATA_PATH
from src.core.downloader import download_files, get_filelist_from_index
from src.database import models
from src.database.base import Base
from src.database.engine import Session, engine
from src.updater import strategies


def get_all_models():
    # models need to be imported so that they are registered
    # on the Base metadata instance.
    # We technically import them in the top part of the file, but for
    # clarity purposes, we repeat it in here.
    from src.database import models  # noqa: F401

    return [cast(Type[Base], mapper.class_) for mapper in Base.registry.mappers]


def get_models_with_loader_info():
    return [
        model_cls for model_cls in get_all_models() if model_cls.loader_info is not None
    ]


def update_tables(tablenames: Optional[list[str]] = None):
    models_to_update = [*get_models_with_loader_info()]

    # Filter out models by the given tablenames, in case we would
    # only want to update a single table (for testing purposes)
    if tablenames is not None and tablenames:
        models_to_update = [
            model_cls
            for model_cls in models_to_update
            if model_cls.__tablename__ in tablenames
        ]
        logger.debug(f"Filtered out tables, only updating {models_to_update!r}")

    with Session() as session:
        # Disable FK checks
        if "postgresql" == engine.dialect.name:
            for model_cls in get_all_models():
                session.execute(
                    sa.text(
                        f"ALTER TABLE {model_cls.__tablename__} DISABLE TRIGGER ALL"
                    )
                )

        # if specific tables to update are given, we only clear them
        # otherwise, we clear the whole database.
        if tablenames is not None and tablenames:
            for model_cls in models_to_update:
                session.query(model_cls).delete(synchronize_session=False)
        else:
            for model_cls in get_all_models():
                session.query(model_cls).delete(synchronize_session=False)

        logger.info("Start updating tables...")
        start_dt = datetime.datetime.now(datetime.UTC)

        # Start inserting all objects based on the defined strategy of the model
        for model_cls in models_to_update:
            logger.info(f"Updating {model_cls.__tablename__}")

            loader_info = model_cls.loader_info
            assert loader_info is not None

            strategy = (
                loader_info.loader_strategy
                if loader_info.loader_strategy is not None
                else strategies.default
            )
            for insert_model_cls, mappings in strategy(model_cls, loader_info):
                logger.debug(
                    f"got {len(mappings)} rows for {insert_model_cls.__tablename__}"
                )
                if not mappings:
                    continue
                session.execute(sa.insert(insert_model_cls), mappings)

                if loader_info.include_in_itemlist and insert_model_cls is model_cls:
                    itemlist_mappings = mappings[:]
                    for mapping in itemlist_mappings:
                        mapping["tablename"] = model_cls.__tablename__

                    session.execute(sa.insert(models.ItemList), itemlist_mappings)

        # Add dummy money object so relationship from e.g randdomboxes -> money work
        # This will fail if we only update tables partially, as it already exists in itemlist,
        # we therefore only add it if needed
        money_query = sa.select(models.ItemList).where(models.ItemList.code == "money")
        if session.scalar(money_query) is None:
            session.add(
                models.ItemList(
                    code="money",
                    tablename="money",
                    name="Gelt",
                    icon="def_004.png",
                )
            )

        update_end_dt = datetime.datetime.now(datetime.UTC)
        logger.success(
            "... finished updating tables in "
            f"{precisedelta(update_end_dt - start_dt)}"
        )

        # Re-Enable FK checks
        if "postgresql" == engine.dialect.name:
            for model_cls in get_all_models():
                session.execute(
                    sa.text(f"ALTER TABLE {model_cls.__tablename__} ENABLE TRIGGER ALL")
                )

        session.commit()

        total_end_dt = datetime.datetime.now(datetime.UTC)
        logger.success(f"Finished in {precisedelta(total_end_dt - start_dt)}")


def fix_fk_violations() -> None:
    # in SQLITE: PRAGMA foreign_key_check;

    queries: list[sa.Select[tuple[Any]]] = [
        # Delete out all item sets that link to an item that does not exist.
        # E.g. Realm Merc Set has a shield with code adsteb101 lol
        sa.select(models.ItemSetItem)
        .outerjoin(models.ItemList)
        .filter(models.ItemList.code.is_(None)),
        # All quest scrolls that link to non existing quests
        sa.select(models.QuestScroll)
        .outerjoin(models.Quest)
        .filter(models.Quest.code.is_(None)),
        # All random boxes with invalid items (rbvip0000 -> mspear105)
        sa.select(models.RandomBox)
        .join(models.RandomBox.rewards)
        .join(models.RandomBoxReward.item, isouter=True)
        .filter(models.ItemList.code.is_(None)),
        # All skill books without skills
        sa.select(models.SkillBook)
        .join(models.SkillBook.skill, isouter=True)
        .where(models.PlayerSkill.code.is_(None)),
        # All store items (looking at you Jeremiah) that link to broken items
        sa.select(models.NpcStoreItem)
        .join(models.NpcStoreItem.item, isouter=True)
        .where(models.ItemList.code.is_(None)),
        # Drops that link to invalid monsters (npcs??)
        sa.select(models.Drop)
        .join(models.Drop.monster, isouter=True)
        .where(models.Monster.code.is_(None)),
        # Quest missions that link to invalid maps
        sa.select(models.QuestMission)
        .join(models.Map, isouter=True)
        .where(models.QuestMission.map_code.isnot(None), models.Map.code.is_(None)),
        # Invalid required skill links to player skill (how tf does that even happen?)
        sa.select(models.PlayerRequiredSkill)
        .join(models.PlayerRequiredSkill.skill, isouter=True)
        .where(models.PlayerSkill.code.is_(None)),
        # Party islands map areas just link to a wrong map code. We just delete the areas, we don't use them anyways
        sa.select(models.MapArea)
        .join(
            models.Map,
            onclause=models.MapArea.map_code == models.Map.code,
            isouter=True,
        )
        .where(models.Map.code.is_(None)),
    ]

    with Session() as session:
        for query in queries:
            for obj in session.scalars(query):
                session.delete(obj)

                insp = sa.inspect(obj)
                pk_keys = [col.name for col in insp.mapper.primary_key]
                pks = ", ".join([repr(getattr(obj, pk)) for pk in pk_keys])

                logger.debug(
                    f"Deleted {obj.__class__.__name__}({pks}) due to foreign key constraints failing."
                )
                session.flush()

        # Some quests have quest scrolls as "start npc", instead of removing them, we just delete the column
        for obj in session.scalars(
            sa.select(models.Quest).join(
                models.QuestScroll,
                onclause=models.Quest.start_npc_code == models.QuestScroll.code,
            )
        ):
            obj.start_npc_code = None
        session.flush()

        # Same for monsters, they may link to non existent skills. We just remove the skill reference from them
        # Right now, there is only one "invalid" skill some sea monsters link to: "mk0001"
        # Skill 1 and Skill 2 are always "mk0001", so we can go by either column
        for obj in session.scalars(
            sa.select(models.Monster).where(models.Monster.skill_1_code == "mk0001")
        ):
            obj.skill_1_code = None
            obj.skill_2_code = None
        session.flush()

        session.commit()


def download_updater_files(skip_existing: bool):
    filelist = get_filelist_from_index()

    required_filenames = list(
        itertools.chain.from_iterable(
            [
                model_cls.loader_info.files.all_files
                for model_cls in get_models_with_loader_info()
                if model_cls.loader_info is not None
            ]
        )
    )
    required_quest_filelist = filelist.find_by_regex(
        re.compile(r"Data\/DataTable\/QuestData\/\w+\.xml")
    )
    required_filenames += [f.filename for f in required_quest_filelist]

    # Check if files are already present, if so, we skip them
    if skip_existing:
        existing_files = os.listdir(UPDATER_DATA_PATH)
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
        if os.path.exists(UPDATER_DATA_PATH):
            shutil.rmtree(UPDATER_DATA_PATH)

    if not os.path.exists(UPDATER_DATA_PATH):
        os.makedirs(UPDATER_DATA_PATH)

    files_to_download = filelist.find_by_filenames(required_filenames)
    download_files(files_to_download, UPDATER_DATA_PATH)
