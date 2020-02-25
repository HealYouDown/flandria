from sqlalchemy import Column, String, Integer
from ...extensions import db


class QuestItem(db.Model):
    __tablename__ = "quest_item"
    __bind_key__ = "static_data"

    index = Column(Integer)
    code = Column(String, primary_key=True)
    name = Column(String)
    icon = Column(String)
    rare_grade = Column(Integer)

    def to_dict(self, minimal: bool = False) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "icon": self.icon,
            "rare_grade": self.rare_grade,
        }
