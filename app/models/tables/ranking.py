from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.extensions import db


class Guild(db.Model):
    __tablename__ = "guild"
    __bind_key__ = "ranking"
    id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    name_hash = Column(String)
    server = Column(String)
    members = relationship("Player")
    number_of_members = Column(Integer)
    avg_rank = Column(Float)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            "id": self.id,
            "name": self.name,
            "name_hash": self.name_hash,
            "server": self.server,
            "number_of_members": self.number_of_members,
            "avg_rank": self.avg_rank
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "members": [p.to_dict() for p in self.members]
        }


class Player(db.Model):
    __tablename__ = "player"
    __bind_key__ = "ranking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rank = Column(Integer)
    name = Column(String)
    class_ = Column(String)
    level_land = Column(Integer)
    level_sea = Column(Integer)
    server = Column(String)
    guild = Column(String, ForeignKey("guild.name"))

    def to_dict(self) -> dict:
        return {
            "rank": self.rank,
            "name": self.name,
            "class": self.class_,
            "level_land": self.level_land,
            "level_sea": self.level_sea,
            "server": self.server,
        }
