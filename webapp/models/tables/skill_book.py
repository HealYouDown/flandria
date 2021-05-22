from webapp.extensions import db
from webapp.models.declarative_mixins import SoldByMixin
from webapp.models.mixins import BaseMixin
from webapp.models.custom_sql_classes import CustomColumn


class SkillBook(
    db.Model, BaseMixin,
    SoldByMixin
):
    __tablename__ = "skill_book"

    _mapper_utils = {
        "files": {
            "server": [
                "s_SkillBookItem.bin"
            ],
            "client": [
                "c_SkillBookItemRes.bin"
            ],
            "string": [
                "SkillBookItemStr.dat"
            ],
        },
    }

    skill_code = CustomColumn(
        db.String(32), db.ForeignKey("player_skill.code"),
        nullable=False, mapper_key="대상코드")

    skill = db.relationship("PlayerSkill", foreign_keys=[skill_code],
                            uselist=False, viewonly=True,)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "skill": self.skill.to_dict() if self.skill else None,
            **SoldByMixin.to_dict(self),
        }
