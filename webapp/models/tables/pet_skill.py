from webapp.extensions import db
from webapp.models.mixins import SkillDataMixin


class PetSkill(db.Model, SkillDataMixin):
    __tablename__ = "pet_skill"

    _mapper_utils = {
        "files": {
            "server": [
                "s_PetSkillAction.bin"
            ],
            "client": [
                "c_PetSkillActionRes.bin"
            ],
            "string": [
                "PetSkillActionStr.dat"
            ],
            "description": [
                "PetSkillActionDesc.dat"
            ],
        },
        "options": {
            "description_key": "코드",
            "image_key": "아이콘코드"
        }
    }

    def to_dict(self) -> dict:
        return SkillDataMixin.to_dict(self)
