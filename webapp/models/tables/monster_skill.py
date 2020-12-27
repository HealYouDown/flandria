from webapp.extensions import db
from webapp.models.mixins import SkillDataMixin


class MonsterSkill(db.Model, SkillDataMixin):
    __tablename__ = "monster_skill"

    _mapper_utils = {
        "files": {
            "server": [
                "s_MobSkillAction.bin"
            ],
            "client": [
                "c_MSkillActionRes.bin"
            ],
            "string": [
                "MSkillActionStr.dat"
            ],
            "description": [
                "MobSkillActionDesc.dat"
            ],
        },
        "options": {
            "image_key": "아이콘코드",
            "description_key": "원형코드"
        }
    }

    def to_dict(self) -> dict:
        return SkillDataMixin.to_dict(self)
