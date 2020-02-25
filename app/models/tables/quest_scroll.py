from sqlalchemy import Column, String, Integer, ForeignKey
from ...extensions import db


class QuestScroll(db.Model):
    __tablename__ = "quest_scroll"
    __bind_key__ = "static_data"

    index = Column(Integer)
    code = Column(String, primary_key=True)
    name = Column(String)
    icon = Column(String)
    rare_grade = Column(Integer)
    quest_code = Column(String, ForeignKey("quest.code"))

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            "code": self.code,
            "name": self.name,
            "icon": self.icon,
            "rare_grade": self.rare_grade,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "quest_code": self.quest_code,
        }
