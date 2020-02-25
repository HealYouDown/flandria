from sqlalchemy import Column, String
from ...extensions import db


class Map(db.Model):
    __tablename__ = "map"
    __bind_key__ = "static_data"

    code = Column(String, primary_key=True)
    name = Column(String)

    def to_dict(self, minimal: bool = False) -> dict:
        return {
            "code": self.code,
            "name": self.name,
        }
