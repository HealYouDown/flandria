from ...extensions import db
from ..mixins import PlayerSkillMixin


class ShipSkill(db.Model, PlayerSkillMixin):
    __tablename__ = "ship_skill"
    __bind_key__ = "static_data"

    def to_dict(self) -> dict:
        return PlayerSkillMixin.to_dict(self)
