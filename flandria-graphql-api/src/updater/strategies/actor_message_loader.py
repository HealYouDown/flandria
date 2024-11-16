from typing import TYPE_CHECKING, cast

from src.core.constants import LANGUAGE
from src.core.enums import MonsterMessageTrigger
from src.updater.file_data import FileData

if TYPE_CHECKING:
    from src.database.types import ModelCls
    from src.updater.schema import LoaderInfo

    from .types import T_STRATEGY_RETURN


def actor_message(
    model_cls: "ModelCls",
    loader_info: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    data = FileData.from_files(loader_info.files)

    trigger_keys = [
        ("Idle0", MonsterMessageTrigger.IDLE),
        ("Idle1", MonsterMessageTrigger.IDLE),
        ("Attack0", MonsterMessageTrigger.ATTACK),
        ("Attack1", MonsterMessageTrigger.ATTACK),
        ("Damage0", MonsterMessageTrigger.DAMAGE),
        ("Damage1", MonsterMessageTrigger.DAMAGE),
        ("Critical0", MonsterMessageTrigger.CRITICAL),
        ("Critical1", MonsterMessageTrigger.CRITICAL),
        ("Die0", MonsterMessageTrigger.DIE),
        ("Die1", MonsterMessageTrigger.DIE),
        ("ObjRegen0", MonsterMessageTrigger.REGENERATION),
        ("ObjRegen1", MonsterMessageTrigger.REGENERATION),
    ]

    objects: list[dict] = []
    for row in data.client_data:
        # row:
        # {
        #     "대사코드": "obchat000",
        #     "Idle0": "obchpld00",
        #     "Idle1": "obchpld01",
        #     "Attack0": "obchpld01",
        #     "Attack1": "obchpld01",
        #     "Damage0": "obchpld01",
        #     "Damage1": "obchpld01",
        #     "Critical0": "obchpld01",
        #     "Critical1": "obchpld01",
        #     "Die0": "obchpld01",
        #     "Die1": "obchpld01",
        #     "ObjRegen0": "obchpld02",
        #     "ObjRegen1": "obchpld03",
        # }
        code = row["대사코드"]
        for trigger_key, trigger in trigger_keys:
            message_code = cast(str, row[trigger_key])
            try:
                message = data.string_lookup[message_code][LANGUAGE]
            except KeyError:
                # A lot of messages are "missing",
                # logging would just spam the console, so we ignore them
                continue

            objects.append(
                {
                    "code": code,
                    "trigger": trigger,
                    "message": message,
                }
            )

    return [(model_cls, objects)]
