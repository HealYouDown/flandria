import os

import sqlalchemy as sa
import sqlalchemy.orm as orm
from loguru import logger

from src.database.engine import engine
from src.database.models import Map, Monster, MonsterPosition, Npc, NpcPosition
from src.updater.parsers import parse_monster_positions, parse_npc_positions

CODE_TO_FOLDER = {
    "AC1_000": "ac1",
    "AF1_000": "af1",
    "AF2_000": "af2",
    "AD1_000": "ad1_1b",
    "AD2_000": "ad1_2b",
    "AD3_000": "ad3_1b",
    "AD4_000": "ad4_1b",
    "AD5_000": "ad5_1b",
    "BC1_000": "bc1",
    "BF1_000": "bf1",
    "BF2_000": "bf2",
    "BD1_000": "bd1_1f",
    "BD2_000": "bd1_1b",
    "BD3_000": "bd1_2b",
    "BC2_000": "bc2",
    "CC1_000": "cc1",
    "CF1_000": "cf1",
    "SR1_000": "sr1",
    "SR2_000": "sr2",
    "SR3_000": "sr3",
    "SD1_000": "sd1",
    "SD2_000": "sd2",
    "SD1F1_000": "sd1f1",
    "SD2F1_000": "sd2f1",
    "CD1_000": "cd1_1b",
    "CD2_000": "cd1_2b",
    "CD3_000": "cd1_3b",
    "CD4_000": "cd1_4b",
    "CD5_000": "cd1_5b",
    "CD6_000": "cd1_6b",
    "CED1_000": "ced_1b",
    "CED2_000": "ced_2b",
    "CED3_000": "ced_3b",
    "CED4_000": "ced_4b",
    "CED5_000": "ced_5b",
    "CED6_000": "ced_6b",
    "AS1_000": "as1",
    "EF1_000": "ef1",
    "EC1_000": "ec1",
    # tower
    # "AT001_000": "at001",
    # "AT002_000": "at002",
    # "AT003_000": "at003",
    # "AT004_000": "at004",
    # "AT005_000": "at005",
    # "AT006_000": "at006",
    # "AT007_000": "at007",
    # "AT008_000": "at008",
    # "AT009_000": "at009",
    # "AT010_000": "at010",
    "AI1_000": "ai1",
    "AI2_000": "ai2",
    "BI1_000": "bi1",
    "BI3_000": "bi3",
    "CI3_000": "ci3",
    "CI5_000": "ci5",
    "EI1_000": "ei1",
    "EI4_000": "ei4",
    "ED1_000": "ed1_1b",
    "ED2_000": "ed1_2b",
    "ED3_000": "ed2_1b",
    "ED4_000": "ed2_2b",
    # Battlefield Maps
    # "AW1_000": "aw1",
    # "BW1_000": "bw1",
    # "CW1_000": "cw1",
    # "EW1_000": "ew1",
    "DF1_000": "df1",
}


def load_maps(maps_folder_path: str) -> None:
    with orm.Session(engine) as session:
        session.query(MonsterPosition).delete(synchronize_session=False)
        session.query(NpcPosition).delete(synchronize_session=False)

        npc_codes = session.scalars(sa.select(Npc.code)).all()
        monster_codes = session.scalars(sa.select(Monster.code)).all()
        maps = session.scalars(sa.select(Map)).all()

        for map in maps:
            if map.code not in CODE_TO_FOLDER:
                logger.warning(
                    f"Skipping {map.name!r} ({map.code!r}) - no mapping found"
                )
                continue

            folder_name = CODE_TO_FOLDER[map.code]
            folder_path = os.path.join(maps_folder_path, folder_name.upper())
            if not os.path.exists(folder_path):
                logger.warning(f"Missing map folder {folder_path!r}")
                continue

            logger.info(f"Loading map {map.name!r} ({map.code!r})")

            npc_fpath = os.path.join(folder_path, f"{folder_name}_dummy_npc.txt")
            monster_fpath = os.path.join(
                folder_path, f"{folder_name}_dummy_monster.txt"
            )

            if os.path.exists(npc_fpath):
                npc_positions = parse_npc_positions(npc_fpath, map.code)
                filtered_npc_positions = []
                for np in npc_positions:
                    npc_code: str = np["npc_code"]
                    if npc_code not in npc_codes:
                        logger.warning(
                            f"Found non existing npc code {npc_code} for map {map.code!r}"
                        )
                        continue
                    filtered_npc_positions.append(np)
                if filtered_npc_positions:
                    session.execute(sa.insert(NpcPosition), filtered_npc_positions)
            else:
                logger.debug(f"no npcs found for {map.name!r} ({map.code!r})")

            if os.path.exists(monster_fpath):
                monster_positions = parse_monster_positions(monster_fpath, map.code)
                filtered_monster_positions = []
                for mp in monster_positions:
                    monster_code: str = mp["monster_code"]
                    if monster_code not in monster_codes:
                        logger.warning(
                            f"Found non existing monster code {monster_code} for map {map.code!r}"
                        )
                        continue
                    filtered_monster_positions.append(mp)
                if filtered_monster_positions:
                    session.execute(
                        sa.insert(MonsterPosition), filtered_monster_positions
                    )
            else:
                logger.debug(f"no monsters found for {map.name!r} ({map.code!r})")

        session.commit()
