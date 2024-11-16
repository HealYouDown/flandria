import asyncio

import sqlalchemy as sa
import sqlalchemy.orm as orm
from loguru import logger

from src.assets.models.convert import (
    convert_actor_model,
    convert_class_and_gender_model,
    convert_weapon_model,
)
from src.core.utils import get_semaphore_limit
from src.database import models
from src.database.engine import engine


def process_monster_models():
    with orm.Session(engine) as session:
        query = sa.select(
            models.Monster.model_name.distinct(),
        ).where(
            models.Monster.model_name.is_not(None),
        )
        model_names = session.scalars(query).all()

    semaphore_limit = get_semaphore_limit()
    logger.info(f"Starting {semaphore_limit} convert tasks for monster models")

    semaphore = asyncio.Semaphore(semaphore_limit)

    loop = asyncio.new_event_loop()
    tasks = [
        loop.create_task(convert_actor_model(semaphore, "monster", model_name))
        for model_name in model_names
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


def process_npc_models():
    with orm.Session(engine) as session:
        query = sa.select(
            models.Npc.model_name.distinct(),
        ).where(
            models.Npc.model_name.is_not(None),
        )
        model_names = session.scalars(query).all()

    semaphore_limit = get_semaphore_limit()
    logger.info(f"Starting {semaphore_limit} convert tasks for npc models")

    semaphore = asyncio.Semaphore(semaphore_limit)

    loop = asyncio.new_event_loop()
    tasks = [
        loop.create_task(convert_actor_model(semaphore, "npc", model_name))
        for model_name in model_names
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


def process_weapon_models():
    with orm.Session(engine) as session:
        query = sa.union(
            sa.select(models.Duals.model_name.distinct()).where(
                models.Duals.model_name.is_not(None)
            ),
            sa.select(models.Rifle.model_name.distinct()).where(
                models.Rifle.model_name.is_not(None)
            ),
            sa.select(models.Cariad.model_name.distinct()).where(
                models.Cariad.model_name.is_not(None)
            ),
            sa.select(models.Rapier.model_name.distinct()).where(
                models.Rapier.model_name.is_not(None)
            ),
            sa.select(models.OneHandedSword.model_name.distinct()).where(
                models.OneHandedSword.model_name.is_not(None)
            ),
            sa.select(models.TwoHandedSword.model_name.distinct()).where(
                models.TwoHandedSword.model_name.is_not(None)
            ),
            sa.select(models.Dagger.model_name.distinct()).where(
                models.Dagger.model_name.is_not(None)
            ),
            sa.select(models.FishingRod.model_name.distinct()).where(
                models.FishingRod.model_name.is_not(None)
            ),
            # Yea shield is technically not a weapon, but also
            # contained in the item_not folder. Armor however has a
            # female and male variant, which is why they are handled differently.
            sa.select(models.Shield.model_name.distinct()).where(
                models.Shield.model_name.is_not(None)
            ),
        )
        model_names = session.scalars(query).all()

    semaphore_limit = get_semaphore_limit()
    logger.info(
        f"Starting {semaphore_limit} convert tasks for wepaon (and shield) models"
    )

    semaphore = asyncio.Semaphore(semaphore_limit)

    loop = asyncio.new_event_loop()
    tasks = [
        loop.create_task(convert_weapon_model(semaphore, model_name))
        for model_name in model_names
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


def process_armor_models():
    with orm.Session(engine) as session:
        query = sa.union(
            sa.select(models.Coat.model_name.distinct()).where(
                models.Coat.model_name.is_not(None)
            ),
            sa.select(models.Pants.model_name.distinct()).where(
                models.Pants.model_name.is_not(None)
            ),
            sa.select(models.Shoes.model_name.distinct()).where(
                models.Shoes.model_name.is_not(None)
            ),
            sa.select(models.Gauntlet.model_name.distinct()).where(
                models.Gauntlet.model_name.is_not(None)
            ),
        )
        model_names = session.scalars(query).all()

    semaphore_limit = get_semaphore_limit()
    logger.info(f"Starting {semaphore_limit} convert tasks for armor models")

    semaphore = asyncio.Semaphore(semaphore_limit)

    loop = asyncio.new_event_loop()
    tasks = [
        loop.create_task(convert_class_and_gender_model(semaphore, model_name, "armor"))
        for model_name in model_names
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


def process_dress_models():
    with orm.Session(engine) as session:
        query = sa.select(
            models.Dress.model_name.distinct().label("model_name"),
            models.Dress.model_variant,
        ).where(models.Dress.model_name.is_not(None))
        dress_models = session.execute(query).all()

    semaphore_limit = get_semaphore_limit()
    logger.info(
        f"Starting {semaphore_limit} convert tasks for dress models {(len(dress_models))}"
    )

    semaphore = asyncio.Semaphore(semaphore_limit)

    loop = asyncio.new_event_loop()
    tasks = [
        loop.create_task(
            convert_class_and_gender_model(
                semaphore,
                model.model_name,
                "dress",
                variant=model.model_variant,
                variant_mesh_name="robe:2",
            )
        )
        for model in dress_models
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


def process_hat_models():
    with orm.Session(engine) as session:
        query = sa.select(
            models.Hat.model_name.distinct().label("model_name"),
            models.Hat.model_variant,
        ).where(models.Hat.model_name.is_not(None))
        hat_models = session.execute(query).all()

    semaphore_limit = get_semaphore_limit()
    logger.info(
        f"Starting {semaphore_limit} convert tasks for hat models ({len(hat_models)})"
    )

    semaphore = asyncio.Semaphore(semaphore_limit)

    loop = asyncio.new_event_loop()
    tasks = [
        loop.create_task(
            convert_class_and_gender_model(
                semaphore,
                model.model_name,
                "hat",
                variant=model.model_variant,
                variant_mesh_name="hair:2",
            )
        )
        for model in hat_models
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


def process_models(groups: list[str] | None):
    mapping = {
        "monster": process_monster_models,
        "npc": process_npc_models,
        "weapon": process_weapon_models,
        "armor": process_armor_models,
        "dress": process_dress_models,
        "hat": process_hat_models,
        # TODO Ship
    }
    if groups is None:
        groups = list(mapping.keys())

    for mtp in groups:
        mapping[mtp]()
