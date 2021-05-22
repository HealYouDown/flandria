from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import DroppedByMixin, RandomBoxMixin
from webapp.models.mixins import BaseMixin


class PetSkillStone(
    db.Model, BaseMixin,
    DroppedByMixin, RandomBoxMixin,
):
    __tablename__ = "pet_skill_stone"

    _mapper_utils = {
        "files": {
            "server": [
                "s_PetSkillStoneItem.bin"
            ],
            "client": [
                "c_PetSkillStoneItemRes.bin"
            ],
            "string": [
                "PetSkillStoneItemStr.dat"
            ],
        }
    }

    skill_code = CustomColumn(db.String(32), db.ForeignKey("pet_skill.code"),
                              nullable=False, mapper_key="대상코드")

    skill_data = db.relationship("PetSkill", foreign_keys=[skill_code],
                                 viewonly=True,)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "skill": self.skill_data.to_dict(),
            **DroppedByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
