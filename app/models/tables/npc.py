from sqlalchemy import Column, String
from ...extensions import db


class NPC(db.Model):
    __tablename__ = "npc"
    __bind_key__ = "static_data"

    code = Column(String, primary_key=True)
    name = Column(String)
    icon = Column(String)

    def to_dict(self, minimal: bool = False) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "icon": self.icon
        }
