from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn


class MonsterMessage(db.Model):
    __tablename__ = "monster_message"

    _mapper_utils = {
        "files": {
            "server": [
            ],
            "client": [
                "c_ObjChat.bin"
            ],
            "string": [
                "ObjChatDesc.dat"
            ],
        },
        "options": {
            "image_key": "모델명"
        },
    }

    code = CustomColumn(db.String(32), primary_key=True,
                        nullable=False, mapper_key="대사코드")

    idle_0 = CustomColumn(db.Text, mapper_key="Idle0")
    idle_1 = CustomColumn(db.Text, mapper_key="Idle1")

    attack_0 = CustomColumn(db.Text, mapper_key="Attack0")
    attack_1 = CustomColumn(db.Text, mapper_key="Attack1")

    damage_0 = CustomColumn(db.Text, mapper_key="Damage0")
    damage_1 = CustomColumn(db.Text, mapper_key="Damage1")

    critical_0 = CustomColumn(db.Text, mapper_key="Critical0")
    critical_1 = CustomColumn(db.Text, mapper_key="Critical1")

    die_0 = CustomColumn(db.Text, mapper_key="Die0")
    die_1 = CustomColumn(db.Text, mapper_key="Die1")

    regen_0 = CustomColumn(db.Text, mapper_key="ObjRegen0")
    regen_1 = CustomColumn(db.Text, mapper_key="ObjRegen1")

    def to_dict(self) -> dict:
        strings = ["idle", "attack", "damage", "critical",
                   "die", "regen"]

        resp = {}
        for string in strings:
            resp[string] = []

            for i in range(0, 2):
                value = getattr(self, f"{string}_{i}")
                if value:
                    resp[string].append(value)

        return resp
