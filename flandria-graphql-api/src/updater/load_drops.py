import os

import sqlalchemy as sa
import sqlalchemy.orm as orm
from loguru import logger

from src.database.engine import engine
from src.database.models import Drop, ItemList, Money, Monster
from src.updater.parsers import parse_dropfile


def load_drops(drops_folder_path: str) -> None:
    with orm.Session(engine) as session:
        # clear drops table, but keep quest items
        session.query(Drop).where(
            Drop.item_code.not_in(
                sa.select(ItemList.code).where(ItemList.tablename == "quest_item")
            )
        ).delete(synchronize_session=False)
        session.query(Money).delete(synchronize_session=False)

        # get monsters and items for validation checks
        # we also only load existing monsters
        monster_codes = session.scalars(sa.select(Monster.code)).all()
        item_codes = set(session.scalars(sa.select(ItemList.code)).all())

        for monster_code in monster_codes:
            drop_fpath = os.path.join(drops_folder_path, f"{monster_code}.xml")

            if not os.path.exists(drop_fpath):
                logger.debug(f"No drop file for {monster_code!r}")
                continue

            logger.info(f"Parsing dropfile for {monster_code!r}")
            item_drops, money = parse_dropfile(drop_fpath, monster_code)

            logger.debug(f"Found {len(item_drops)} drops for {monster_code!r}")

            # Validate that our item codes really exist
            filtered_item_drops = []
            for item_drop in item_drops:
                item_code: str = item_drop["item_code"]
                if item_code not in item_codes:
                    logger.warning(
                        f"Unknown item code {item_code!r} ({monster_code}.xml)"
                    )
                    continue
                filtered_item_drops.append(item_drop)

            logger.debug(f"{len(item_drops)} drops left after filtering")

            if filtered_item_drops:
                session.execute(sa.insert(Drop), filtered_item_drops)

            if money is not None:
                session.execute(sa.insert(Money), money)
            else:
                logger.debug(f"No money information for {monster_code!r}")

        session.commit()
