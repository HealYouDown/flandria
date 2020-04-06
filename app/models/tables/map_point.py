from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db


class MapPoint(db.Model):
    __tablename__ = "map_point"
    __bind_key__ = "unstatic_data"

    index = Column(Integer, primary_key=True, autoincrement=True)

    map_code = Column(String, ForeignKey("map.code"))

    monster_code = Column(String, ForeignKey("monster.code"))
    monster = relationship("Monster", foreign_keys=[monster_code])

    x = Column(Integer)
    y = Column(Integer)
    z = Column(Integer)

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }
