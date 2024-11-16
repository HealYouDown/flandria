import configparser

from src.updater.transforms import ms_to_seconds


def _get_config_parser() -> configparser.ConfigParser:
    return configparser.ConfigParser(
        comment_prefixes=(";", "'", "//"),
        inline_comment_prefixes=(";", "'", "//"),
        strict=False,
        # Required for parsing errors where a comment does
        # not have a comment prefix -> wtf?
        allow_no_value=True,
    )


def parse_monster_positions(
    fpath: str,
    map_code: str,
) -> list[dict]:
    parser = _get_config_parser()
    parser.read(fpath, encoding="euc_kr")

    monster_positions = []
    for section_key in parser.sections():
        if section_key == parser.default_section:
            continue

        section = parser[section_key]

        # Each section is a location where monsters can spawn
        x = float(section["pos.x"])
        y = float(section["pos.y"])
        z = float(section["pos.z"])

        for i in range(int(section["SpawnMonCount"])):
            monster_code = section[f"Code{i}"]
            respawn_time_str = section[f"Term{i}"]

            # Some parsing workarounds
            # DF1: could not convert string to float: '50000 [spaces] 리젠타임'
            respawn_time_str = respawn_time_str.split(" ")[0]
            respawn_time = int(ms_to_seconds(int(float(respawn_time_str))))

            # mtgalmae1 has a location with a respawn time of 30000000000 (^= 951 Years)
            # GraphQL only supports ints up to signed 32-bit
            if respawn_time >= 2**31 - 1:
                respawn_time = 2**31 - 1

            monster_positions.append(
                {
                    "map_code": map_code,
                    "monster_code": monster_code,
                    "amount": int(section[f"Num{i}"]),
                    "respawn_time": respawn_time,
                    "x": x,
                    "y": y,
                    "z": z,
                }
            )

    return monster_positions


def parse_npc_positions(
    fpath: str,
    map_code: str,
) -> list[dict]:
    parser = _get_config_parser()
    parser.read(fpath, encoding="euc_kr")

    npc_positions = []
    for section_key in parser.sections():
        if section_key == parser.default_section:
            continue

        section = parser[section_key]
        npc_code = section["contents"]

        npc_positions.append(
            {
                "npc_code": npc_code,
                "map_code": map_code,
                "x": float(section["pos.x"]),
                "y": float(section["pos.y"]),
                "z": float(section["pos.z"]),
            }
        )

    return npc_positions
