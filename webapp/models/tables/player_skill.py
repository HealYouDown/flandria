from webapp.extensions import db
from webapp.models.mixins import SkillDataMixin


class PlayerSkill(db.Model, SkillDataMixin):
    __tablename__ = "player_skill"

    _mapper_utils = {
        "files": {
            "server": [
                "s_CharSpellAction.bin",
                "s_CharSkillAction.bin",
                "s_ShipSkillAction.bin",
            ],
            "client": [
                "c_SpellActionRes.bin",
                "c_SkillActionRes.bin",
                "c_ShipSkillActionRes.bin",
            ],
            "string": [
                "SpellActionStr.dat",
                "SkillActionStr.dat",
                "ShipSkillActionStr.dat",
            ],
            "description": [
                "CharSpellActionDesc.dat",
                "CharSkillActionDesc.dat",
                "ShipSkillActionDesc.dat",
            ],
        },
        "options": {
            "image_key": "아이콘코드",
            "description_key": "코드",
        }
    }

    def to_dict(self, minimal: bool = False) -> dict:
        return SkillDataMixin.to_dict(self, minimal)
